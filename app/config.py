from pydantic_settings import BaseSettings

from dotenv import load_dotenv





class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    ALGORITHM: str
    KEY: str

    class ConfigDict:
        _env_file = ".env"



load_dotenv()

settings = Settings()