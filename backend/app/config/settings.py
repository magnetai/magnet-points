# app/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    ADMIN_ADDRESS: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()