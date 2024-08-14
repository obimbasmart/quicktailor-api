
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    BASE_URL: str
  
    class Config:
        env_file = '.env'
        extra = 'allow'

class TestSettings(Settings):
    TEST_PUBLIC_KEY: str
    TEST_SECRET_KEY: str


settings = TestSettings()