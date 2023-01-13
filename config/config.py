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

    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_HOST_LOCAL: str = Field(..., env="POSTGRES_HOST_LOCAL")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")

    API_PATH_V1: str = "/api/v1/"

    SUPERUSER_EMAIL: str = Field(..., env="SUPERUSER_EMAIL")
    SUPERUSER_PHONE: str = Field(..., env="SUPERUSER_PHONE")
    SUPERUSER_PASSWORD: str = Field(..., env="SUPERUSER_PASSWORD")

    USER_EMAIL: str = Field(..., env="USER_EMAIL")
    USER_PHONE: str = Field(..., env="USER_PHONE")
    USER_PASSWORD: str = Field(..., env="USER_PASSWORD")

    TIME_ZONE: str = 'Europe/Moscow'

    MAILER_MAIL_USERNAME: str = Field(..., env="MAILER_MAIL_USERNAME")
    MAILER_MAIL_PASSWORD: str = Field(..., env="MAILER_MAIL_PASSWORD")
    MAILER_MAIL_FROM: str = Field(..., env="MAILER_MAIL_FROM")
    MAILER_MAIL_SERVER: str = Field(..., env="MAILER_MAIL_SERVER")
    MAILER_MAIL_FROM_NAME: str = Field(..., env="MAILER_MAIL_FROM_NAME")

    TRACKING_EMAIL: str = Field(..., env="TRACKING_EMAIL")
    PASSWORD_TRACKING_EMAIL: str = Field(..., env="PASSWORD_TRACKING_EMAIL")
    IMAP4_SSL: str = Field(..., env="IMAP4_SSL")

    CHECKMOBI_TOKEN: str = Field(..., env="CHECKMOBI_TOKEN")

    ADMIN_TEST_INITIAL_USER_EMAIL: str = Field(..., env="ADMIN_TEST_INITIAL_USER_EMAIL")
    ADMIN_TEST_INITIAL_USER_PASSWORD: str = Field(..., env="ADMIN_TEST_INITIAL_USER_PASSWORD")

    PLAIN_TEST_INITIAL_USER_EMAIL: str = Field(..., env="PLAIN_TEST_INITIAL_USER_EMAIL")
    PLAIN_TEST_INITIAL_USER_PASSWORD: str = Field(..., env="PLAIN_TEST_INITIAL_USER_PASSWORD")

    UNSUBSCRIBED_API_URL: str = Field(..., env="UNSUBSCRIBED_API_URL")

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