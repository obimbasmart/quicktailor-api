from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str = 'AKIAYS2NRXIE7VU37K5J'
    AWS_SECRET_ACCESS_KEY: str = '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'
    S3_BUCKET_NAME: str = 'qt-product-bucket'
    REGION_NAME: str = 'eu-north-1'
    
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