import os

from dotenv import load_dotenv

from backend.app.utils.exception import UnknownEnviromentError
from shared.config.settings import DevelopmentSettings, ProductionSettings


def get_settings() -> DevelopmentSettings | ProductionSettings:
    load_dotenv()
    env = os.getenv("ENV", "development")

    if env == "development":
        return DevelopmentSettings()
    if env == "production":
        return ProductionSettings()
    raise UnknownEnviromentError(f"Неизвестная среда: {env}")
