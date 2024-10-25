# app/__init__.py
import logging
from app.config.settings import settings
from app.core.redis_client import redis_client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

__all__ = ['settings', 'redis_client']
