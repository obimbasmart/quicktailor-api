from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ADMIN_SSO: str

    class Config:
        env_file = '.env'
        extra = 'allow'

class TestSettings(Settings):
    DATABASE_URI: str = "sqlite:///./qt_test_message_app.db"

class DevSettings(Settings):
    DATABASE_URI: str = "sqlite:///./sql_message_app.db"

class ProdSettings(Settings):
    DATABASE_URI: str = 'olegbyonic'


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


