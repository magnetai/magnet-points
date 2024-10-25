from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.point_calculator import PointCalculator
from app.services.point_service import PointService
import time

from app.config.logger import get_logger

logger = get_logger(__name__)

class PointScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.calculate_hourly_points,
            CronTrigger(minute="*"),  # Executed at the top of every hour
            id='calculate_points'
        )

    def calculate_hourly_points(self):
        """​Scoring task executed once every hour"""
        try:
            logger.info("Start calculating hourly scores")
            point_service = PointService()
            point_service.initialize_user_points()
            calculator = PointCalculator()
            start_time = calculator.get_last_processed_time()
            current_time = int(time.time())
            
            # Calculate the scores for this time period
            calculator.process_user_messages(start_time, current_time)
            
            # Update last processing time
            calculator.update_last_processed_time(current_time)
            
        except Exception as e:
            logger.info(f"Error in calculating hourly points : {e}")

    def start(self):
        """Start scheduler"""
        self.scheduler.start()

    def shutdown(self):
        """Close scheduler"""
        self.scheduler.shutdown()