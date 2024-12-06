from pydantic_settings import BaseSettings, SettingsConfigDict
import os

dotenv = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=dotenv, extra='allow')

settings = Settings()