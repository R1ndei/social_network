import os
from functools import lru_cache

import pytz as pytz
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_TITLE: str = "ESB"
    PROJECT_VERSION: str = "0.0.0.1"

    IM_API_TITLE: str = "IM-API"
    IM_API_VERSION: str = "0.1"
    IM_API_PATH = "/im/api/"
    API_PATH_V1: str = "/api/v1/"
    TIME_ZONE: str = 'Europe/Moscow'

    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_HOST_LOCAL: str = Field(..., env="POSTGRES_HOST_LOCAL")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")

    HUNTER_API_KEY: str = Field(..., env="HUNTER_API_KEY")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_database_url(self) -> str:
        """
        Получение полного пути до БД.
        :return: Строка URL.
        """
        url: str = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}_test" if os.environ.get(
            "TESTING") == "1" else f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url

    def get_local_database_url(self) -> str:
        """
        Получение полного пути до БД.
        :return: Строка URL.
        """

        url: str = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}_test" if os.environ.get(
            "TESTING") == 1 else f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url


@lru_cache()
def main_settings() -> callable:
    return Settings()


time_zone = pytz.timezone(main_settings().TIME_ZONE)
