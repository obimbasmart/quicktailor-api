from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_NAME: str
    ENVIRONMENT: str
    REGION_NAME: str

    class Config:
        env_file = '.env'
    
class TestSettings(Settings):
    pass

class DevSettings(Settings):
    pass

class ProdSettings(BaseSettings):
    pass


def get_settings() -> Settings:
    settings = DevSettings()
    if getenv('ENVIRONMENT') == 'testings':
        return TestSettings()
    return settings