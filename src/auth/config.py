from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class AuthSettings(BaseSettings):
    SECRET_KEY : str  = "3b4e13f80aaa605d62035ba72fd6156e189f0f5694d3d45090c6d98d5cde39e4"
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(minutes=120)

settings = AuthSettings()