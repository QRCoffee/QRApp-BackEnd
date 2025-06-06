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
    APP_VERSION: str = "0.1.0"

    # Secret
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ACCESS_KEY: str
    REFRESH_KEY: str
    # FrontEnd
    FRONTEND_HOST:HttpUrl = "http://localhost:5173"
    # Database
    MYSQL_HOST:str = "127.0.0.1"
    MYSQL_PORT:int = 3306
    MYSQL_USERNAME:str | None = None
    MYSQL_PASSWORD:str | None = None
    MYSQL_DATABASE:str = "QRApp"
    # Session
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DATABASE:int = 0
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def MYSQL_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USERNAME,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            path=str(self.MYSQL_DATABASE)
        )
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="redis",
            username=self.REDIS_USERNAME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=str(self.REDIS_DATABASE)
        )
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
            level=self.LOG_LEVEL,
        )
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        logger.add(
            self.LOG_FILE,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level=self.LOG_LEVEL,
            encoding="utf-8",
            rotation="50 MB",  # Option: Rotate (reset) log file after reaching 50 MB
            retention="7 days",  # Keep rotated log files (including zipped) for 7 days
            compression="zip"  # Compress old log files into zip format
        )
        return self
settings = Settings()