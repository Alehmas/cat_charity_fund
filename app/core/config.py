from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Settings class with a list of variables used in the application."""

    app_title: str = 'QRKot application'
    app_description: str = 'Application for the Cat Charitable Foundation'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'FIRST_SUPERUSER_EMAIL'
    first_superuser_password: Optional[str] = 'FIRST_SUPERUSER_PASSWORD'

    class Config:
        env_file = '.env'


settings = Settings()
