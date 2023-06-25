from pydantic import BaseSettings
from functools import lru_cache
# import secrets
# secret_key = secrets.token_urlsafe(32)
# print(secret_key)



class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"
        
@lru_cache()
def get_settings():
    return Settings()