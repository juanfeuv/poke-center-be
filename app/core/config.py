from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    APPLICATION_NAME: str = "POKE-CENTER-BE"
    APP_NAME: str = "FastApi"
    API_VERSION: str = "/api/v1"
    DATABASE = "poke-center"
    DB_ALIAS = "poke-center"
    MONGODB_URI: str = "mongodb+srv://pokeuser:agJcdVUFViyiztKy@poke-center.yvoqajr.mongodb.net/"
    TOKEN_EXPIRY = 10080
    ALGORITHM = "HS256"
    SECRET_KEY = "3426058954gadfsgkfdpghuirbajwf40856s"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()