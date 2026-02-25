from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str
    MT5_API_KEY: str
    ADMIN_PASSWORD: str

    ENV: str = Field(default="development")

    class Config:
        env_file = ".env"
        case_sensitive = True
    
settings = Settings()