import logging
import os
from typing import Annotated, Any, Literal

from pydantic import BeforeValidator, HttpUrl, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    @staticmethod
    def _parse_cors(v: Any) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)
    # Application
    APP_NAME: str = "QRApp Backend"
    APP_VERSION: str = "0.1.0"
    @computed_field  # type: ignore[prop-decorator]
    @property
    def APP_HOST(self) -> str:
        if self.ENVIRONMENT == "localhost":
            return "127.0.0.1"
        return "0.0.0.0"
    # Enviroment - Secret
    ENVIRONMENT: Literal["localhost", "production"] = "localhost"
    # Secret
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ACCESS_KEY: str | None = None 
    JWT_REFRESH_KEY: str | None = None
    BACKEND_CORS_ORIGINS: Annotated[
        list[HttpUrl] | str, 
        BeforeValidator(_parse_cors)
    ] = []
    # FrontEnd
    FRONTEND_HOST:HttpUrl = "http://localhost:5173"
    # Database
    MYSQL_HOST:str = "127.0.0.1"
    MYSQL_PORT:str = "3306"
    MYSQL_USERNAME:str | None = None
    MYSQL_PASSWORD:str | None = None
    MYSQL_DATABASE:str = "QRApp"
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]
    # Logging
    LOG_NAME: str = "QRApp"
    LOG_FILE: str | None = None
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    
    @model_validator(mode="after")
    def config_logging(self) -> Self:
        # Config 
        handlers: list[Any] = [logging.StreamHandler()]
        if self.LOG_FILE:
            os.makedirs(os.path.dirname(self.LOG_FILE),exist_ok=True)
            handlers.append(logging.FileHandler(self.LOG_FILE, encoding='utf-8'))
        logging.basicConfig(
            level=self.LOG_LEVEL,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            handlers=handlers
        )
        return self
settings = Settings()