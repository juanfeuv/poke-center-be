import os


from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()

class Settings(BaseSettings):
    APPLICATION_NAME: str = "POKE-CENTER-BE"
    APP_NAME: str = "FastApi"
    API_VERSION: str = "/api/v1"
    DATABASE = "poke-center"
    DB_ALIAS = "poke-center"
    MONGODB_URI: str = os.environ.get('CONNECCTION_STRING') | ""
    TOKEN_EXPIRY = 10080
    ALGORITHM = "HS256"
    SECRET_KEY = "3426058954gadfsgkfdpghuirbajwf40856s"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
