from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_URL: str
    PASSWORD: str

settings_object = Settings()  # type: ignore[call-arg]
