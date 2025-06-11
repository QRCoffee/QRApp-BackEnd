import os
from typing import Literal

from loguru import logger
from pydantic import HttpUrl, computed_field, model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # Application
    APP_NAME: str = "QRApp Backend"
    APP_VERSION: str = "1.0.0"
    # Secret
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ACCESS_KEY: str = "1"
    REFRESH_KEY: str = "1"
    # FrontEnd
    FRONTEND_HOST:HttpUrl = "http://localhost:5173"
    # Database
    MONGO_URL: str | None = None
    MONGO_DATABASE:str = "QRApp"
    # Session
    REDIS_URL: str | None = None
    # ADMIN ACOUNT
    ADMIN_USERNAME:str = "admin"
    ADMIN_PASSWORD:str = "admin"
    # Logging
    LOG_FILE: str = "./logs/app.log"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    
    @model_validator(mode="after")
    def config_logging(self) -> Self:
        logger.remove()
        # Config 
        logger.add(
            sink=lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            colorize=True,
            enqueue = True,
            level=self.LOG_LEVEL,
        )
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        logger.add(
            self.LOG_FILE,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level=self.LOG_LEVEL,
            enqueue = True,
            encoding="utf-8",
            rotation="50 MB",  # Option: Rotate (reset) log file after reaching 50 MB
            retention="7 days",  # Keep rotated log files (including zipped) for 7 days
            compression="zip"  # Compress old log files into zip format
        )
        return self
settings = Settings()