from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str= "70a89617b0e246cbb1a7357c94f39eb0"

class TestSettings(BaseSettings):
    DATABASE_URI: str = "sqlite:///./qt_test_app.db"

class DevSettings(Settings):
    DATABASE_URI: str = "sqlite:///./sql_app.db"

class ProdSettings(Settings):
    DATABASE_URI: str = "postgresql://user:password@postgresserver/db"


settings = {
    "testing" : TestSettings(),
    "development" : DevSettings(),
    "production" : ProdSettings(),
}

def get_settings():
    env = os.getenv('ENVIRONMENT')
    if env:
        return settings[env]
    return Settings()
    