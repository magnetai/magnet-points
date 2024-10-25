# app/services/score_service.py
from app.core.redis_client import redis_client
import time
from typing import Dict, List, Optional

from app.services.point_calculator import PointCalculator
from app.models.schemas import UserPoints
from app.config.logger import get_logger

logger = get_logger(__name__)

point_calculator = PointCalculator()

def format_eth_address(address: str) -> str:
    try:
        # Check the length of the address to make sure it is a valid Ethereum address
        if len(address) != 42 or not address.startswith("0x"):
            raise ValueError("Invalid Ethereum address")
        
        # Take the first 6 digits and the last 4 digits, and replace them with ellipsis
        return f"{address[:6]}....{address[-4:]}"
    except Exception as e:
        return address

class PointService:
    def __init__(self):
        self.redis_client = redis_client.client
        self.leaderboard_key = "user:points"
        self.T1_POINTS_KEY = "user:t1_points:{}"  # Hash stores user t1 score

    def init_t1_points(self, t1_points: List[UserPoints]):
        # Initialize T1 score using HSET command
        for t1_point in t1_points:
            user_id = t1_point.user_id.lower()
            t1_point_key = self.T1_POINTS_KEY.format(user_id)
            self.redis_client.hset(t1_point_key, "points", t1_point.points)
            self.redis_client.hset(t1_point_key, "is_initialized", 0)
            try:
                points = self.redis_client.zscore(self.leaderboard_key, user_id)
                if points is not None:
                    self.redis_client.zadd(self.leaderboard_key, {user_id: 0})
            except Exception as e:
                logger.error(f"Error in init_t1_points: {e}")
                pass
        return True

    def update_user_point(self, user_points: List[UserPoints]):
        for user_point in user_points:
            user_id = user_point.user_id.lower()
            points = user_point.points
            points_in_db = point_calculator.get_points(user_id)
            if points_in_db is None:
                self.redis_client.zadd(self.leaderboard_key, {user_id: points})
            else:
                self.redis_client.zincrby(self.leaderboard_key, points, user_id)
        return True

    def initialize_user_points(self):
        # Use SCAN command to get all keys starting with 'user:account:'
        cursor = 0
        while True:
            cursor, keys = self.redis_client.scan(cursor, match='user:account:*')
            # Loop through the found keys, extract the user_id and initialize the score

            for key in keys:
                # Extract user_id, assuming user_id is the last part of the key name
                user_id = key.split(':')[-1]
                user_id = user_id.lower()
                points_in_db = point_calculator.get_points(user_id)
                if points_in_db is None:
                    self.redis_client.zadd(self.leaderboard_key, {user_id: 10})
            
            # If the cursor is 0, it means that all keys have been traversed
            if cursor == 0:
                break

    def get_user_points(self, user_id: str) -> Dict:
        user_id = user_id.lower()
        rank = self.redis_client.zrevrank(self.leaderboard_key, user_id)
        point = self.redis_client.zscore(self.leaderboard_key, user_id)
        
        t1_point_key = self.T1_POINTS_KEY.format(user_id)
        t1_point = self.redis_client.hget(t1_point_key, "points")
        
        user_rank = {
            "user_id": format_eth_address(user_id),
            "ardio_points": point,
            "rank": rank + 1 if rank is not None else None,  # Redis rank starts from 0
            "t1_points": t1_point
        }
        return user_rank

    async def get_leaderboard(self, page_index: int = 1, page_size: int = 10, 
                            user_id: Optional[str] = None) -> Dict:
        """
        Get points ranking list
        """
        try:
            # Get the total number of users
            total_users = self.redis_client.zcard(self.leaderboard_key)

            start_index = (page_index - 1) * page_size
            end_index = start_index + page_size - 1
            
            # Get ranking data
            leaderboard_data = self.redis_client.zrevrange(
                self.leaderboard_key, 
                start_index, 
                end_index, 
                withscores=True
            )

            # Build a leaderboard list
            leaderboard = []
            for rank, (uid, point) in enumerate(leaderboard_data, start=1):
                leaderboard.append({
                    "user_id": format_eth_address(uid),
                    "point": int(point),
                    "rank": rank
                })

            # If user_id is specified, obtain the ranking information of the user
            user_rank = None
            if user_id:
                rank = self.redis_client.zrevrank(self.leaderboard_key, user_id)
                if rank is not None:
                    point = self.redis_client.zscore(self.leaderboard_key, user_id)                    
                    user_rank = {
                        "user_id": format_eth_address(user_id),
                        "point": int(point),
                        "rank": rank + 1  # Redis rank starts from 0
                    }

            return {
                "total_users": total_users,
                "leaderboard": leaderboard,
                "user_rank": user_rank
            }

        except Exception as e:
            logger.error(f"Error in get_leaderboard: {e}")
            return {
                "total_users": 0,
                "leaderboard": [],
                "user_rank": None,
                "error": str(e)
            }