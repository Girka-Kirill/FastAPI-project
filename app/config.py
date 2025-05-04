"""
Настройки приложения (секретные ключи, параметры БД и т.д)
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Класс с настройками приложения
    """
    SECRET_KEY: str = "secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """
        Класс для виртуальной среды
        """
        env_file = ".env"

settings = Settings()
