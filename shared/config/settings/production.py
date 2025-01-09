from os import environ
from pydantic_settings import BaseSettings
from shared.config.base import production as base_settings


class ProductionSettings(BaseSettings):
    ENV: str = environ.get("ENV", base_settings.ENV)

    PATH_PREFIX: str = environ.get("PATH_PREFIX", base_settings.PATH_PREFIX)

    APP_HOST: str = environ.get("APP_HOST", base_settings.APP_HOST)
    APP_PORT: int = int(environ.get("APP_PORT", base_settings.APP_PORT))

    DATABASE_NAME: str = environ.get("DATABASE_NAME", base_settings.DATABASE_NAME)
    DATABASE_HOST: str = environ.get("DATABASE_HOST", base_settings.DATABASE_HOST)
    DATABASE_USER: str = environ.get("DATABASE_USER", base_settings.DATABASE_USER)
    DATABASE_PORT: int = int(environ.get("DATABASE_PORT", base_settings.DATABASE_PORT))
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD", base_settings.DATABASE_PASSWORD)

    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", base_settings.DB_CONNECT_RETRY)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", base_settings.DB_POOL_SIZE)
    
    BOT_API_TOKEN: str = environ.get("BOT_API_TOKEN")
    
    YA_GPT_FOLDER_ID: str = environ.get("YA_GPT_FOLDER_ID")
    YANDEX_CLOUD_OAUTH_TOKEN: str = environ.get("YANDEX_CLOUD_OAUTH_TOKEN")
    YANDEX_CLOUD_SERVICE_ACCOUNT_API_KEY: str = environ.get("YANDEX_CLOUD_SERVICE_ACCOUNT_API_KEY")
    
    @property
    def database_settings(self) -> dict[str, str | int]:
        return {
            "database": self.DATABASE_NAME,
            "user": self.DATABASE_USER,
            "password": self.DATABASE_PASSWORD,
            "host": self.DATABASE_HOST,
            "port": self.DATABASE_PORT,
        }

    @property
    def database_uri(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}?gssencmode".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
