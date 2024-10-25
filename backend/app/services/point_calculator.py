from typing import Optional
from app.core.redis_client import redis_client
from datetime import datetime

from app.config.logger import get_logger

logger = get_logger(__name__)

class PointCalculator:
    def __init__(self):
        self.redis = redis_client.client
        self.POINT_KEY = "user:points"  # Sorted Set stores user scores
        self.USER_DETAILS_KEY = "user:details:{}"  # Hash Store user details
        self.LAST_PROCESSED_TIME_KEY = "points_last_processed_time"
        self.USER_LAST_ACTION_DAY = "user:last_action_day:{}"  # stores user daily activity information
        self.T1_POINTS_KEY = "user:t1_points:{}"  # Hash stores user t1 score

    def get_last_processed_time(self) -> int:
        """Get the timestamp of last processing"""
        last_time = self.redis.get(self.LAST_PROCESSED_TIME_KEY)
        if not last_time:
            return None
        return int(last_time)
    
    def init_points(self, address: str):
        """Initialize points"""
        try:
            self.redis.zadd(self.POINT_KEY, { address: 10})
        except Exception as e:
            logger.info(f"Error initializing points: {e}")
    
    def set_last_processed_time(self, timestamp: int):
        """Set the last processed timestamp"""
        self.redis.set(self.LAST_PROCESSED_TIME_KEY, timestamp)
    
    def add_or_update_points(self, address: str, points: float) -> bool:
        """
        Add or update points for an address
        :param address: User address
        :param points: Number of points
        :return: Is it successful?
        """
        logger.info(f"Adding or updating points for address {address} with points {points}")
        points_in_db = self.get_points(address)
        
        if points_in_db is None:
            self.init_points(address)
            
        self.increment_points(address, points)

    def get_points(self, address: str) -> Optional[float]:
        """
        Get points for a specified address
        :param address: User address
        :return: The number of points, if the address does not exist, return None
        """
        points = self.redis.zscore(self.POINT_KEY, address)
        return float(points) if points is not None else None
    
    def increment_points(self, address: str, increment: float) -> Optional[float]:
        """
        Increase the points of the specified address
        :param address: User address
        :param increment: Increased number of points
        :return: Total points after increase
        """
        try:
            return float(self.redis.zincrby(self.POINT_KEY, increment, address))
        except Exception as e:
            logger.error(f"Error incrementing points: {e}")
            return None

    def update_last_processed_time(self, timestamp: int):
        """Update the last processed timestamp"""
        self.redis.set(self.LAST_PROCESSED_TIME_KEY, timestamp)

    def handle_action_message(self, user_id: str, timestamp: int):
        """Update the date of the last action performed by the user"""
        user_action_day_key = self.USER_LAST_ACTION_DAY.format(user_id)
        last_action_day = str(self.redis.get(user_action_day_key))
        action_day = str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d'))
        last_action_time = datetime.strptime(last_action_day, "%Y-%m-%d")
        current_action_time = datetime.strptime(action_day, "%Y-%m-%d")
        if last_action_day is None or current_action_time > last_action_time:
            logger.info(f"Updating last action day for user {user_id} to {action_day}")
            self.redis.set(user_action_day_key, action_day)
            return 10
        else:
            return 5

    def calculate_message_point(self, user_id: str, content: str, timestamp: int) -> int:
        """Calculate the score of a single message"""
        base_point = 0
        try:
            content_array = eval(content)
            if isinstance(content_array, list):
                if len(content_array) > 1:
                    for content_obj in content_array:
                        if content_obj['type'] == 'chat':
                            base_point += 1
                        else:
                            point = self.handle_action_message(user_id, timestamp)
                            base_point += point
                else:
                    content_obj = content_array[0]
                    if content_obj['type'] != 'chat':
                        point = self.handle_action_message(user_id, timestamp)
                        base_point += point
                    else:
                        base_point += 1
        except Exception as e:
            logger.error(f"Error calculating message score for user {user_id}: {e}")
                
        return int(base_point)

    def process_user_messages(self, start_time: int = None, end_time: int = None):
        """Process user messages within a specified time period"""
        # Use Redis search to query messages in a specified time period
        query_parts = []

        if start_time is not None:
            query_parts.append(f'@timestamp:[{start_time} {end_time}]')
        else:
            query_parts.append(f'@timestamp:[-inf {end_time}]')
        
        query = ' '.join(query_parts)

        logger.info(f"Processing messages with query: {query}")
        
        # Use a cursor to iterate through all results
        cursor = 0
        user_points = {}
        
        while True:
            result = self.redis.execute_command(
                'FT.SEARCH', 'historyIndex', query,
                'NOCONTENT',
                'SORTBY', 'timestamp', 'ASC',
                'LIMIT', cursor, 1000
            )
            
            if cursor == 0:
                total_results = result[0]
            
            # Process this batch of messages
            for message_key in result[1:]:
                message_data = self.redis.hgetall(message_key)
                logger.info(f"message_data: {message_data}")
                if not message_data:
                    continue
                role = message_data['role']
                if role != 'ai':
                    continue
                user_id = message_data['user_id']
                content = message_data['content']                
                timestamp = int(message_data['timestamp'])
                
                point = self.calculate_message_point(user_id, content, timestamp)
                
                if user_id not in user_points:
                    user_points[user_id] = {
                        'point': 0,
                        # 'message_count': 0
                    }
                
                user_points[user_id]['point'] += point
                # user_points[user_id]['message_count'] += 1
            
            cursor += len(result) - 1
            if cursor >= total_results:
                break

        # pipeline = self.redis.pipeline()
        for user_id, data in user_points.items():
            points = self.redis.zscore(self.POINT_KEY, user_id)
            logger.info(f"Points in db: {points}")
            if points is None:
                increment = float(data['point']) + 10
                self.redis.zadd(self.POINT_KEY, {user_id: increment})
            else:
                # query from t1 points
                t1_points = self.redis.hgetall(self.T1_POINTS_KEY.format(user_id))
                
                logger.info(f"t1_points: {t1_points}")
                if not t1_points:
                    increment = data['point']
                    self.redis.zincrby(self.POINT_KEY, float(increment), user_id)
                else:
                    t1_is_initialized = t1_points['is_initialized']
                    logger.info(f"t1_is_initialized: {t1_is_initialized}")
                    t1_is_initialized = bool(int(t1_is_initialized))
                    if not t1_is_initialized:
                        self.redis.hset(self.T1_POINTS_KEY.format(user_id), 'is_initialized', 1)
                        increment = float(data['point']) + 10
                        self.redis.zincrby(self.POINT_KEY, increment, user_id)
                    else:
                        increment = data['point']
                        self.redis.zincrby(self.POINT_KEY, increment, user_id)
                        
        # pipeline.execute()