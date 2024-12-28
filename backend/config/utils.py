import os
from dotenv import load_dotenv
from backend.config.settings import DevelopmentSettings, ProductionSettings
from backend.app.utils.exception import UnknownEnviroment



def get_settings() -> DevelopmentSettings | ProductionSettings:
    load_dotenv()
    env = os.getenv("ENV", "development")
    
    if env == "development":
        return DevelopmentSettings()
    if env == "production":
        return ProductionSettings()
    raise UnknownEnviroment(f"Неизвестная среда: {env}")