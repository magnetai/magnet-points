# app/core/redis_client.py
import redis
from app.config.settings import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

redis_client = RedisClient()