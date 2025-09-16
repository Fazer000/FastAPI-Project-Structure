"""Настройки приложения."""

from typing import Optional, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Основные настройки
    PROJECT_NAME: str = Field(default="FastAPI App", description="Название проекта")
    VERSION: str = Field(default="0.1.0", description="Версия приложения")
    DESCRIPTION: str = Field(default="FastAPI приложение", description="Описание API")
    ENVIRONMENT: str = Field(default="development", description="Окружение")
    API_V1_STR: str = Field(default="/api/v1", description="Префикс API v1")
    
    # Совместимость со старыми названиями
    app_name: str = Field(default="FastAPI App", description="Название приложения")
    debug: bool = Field(default=False, description="Режим отладки")
    version: str = Field(default="0.1.0", description="Версия приложения")
    
    # Настройки сервера
    host: str = Field(default="0.0.0.0", description="Хост сервера")
    port: int = Field(default=8000, description="Порт сервера")
    
    # Настройки базы данных
    database_url: Optional[str] = Field(
        default=None, 
        description="URL подключения к базе данных"
    )
    
    # Настройки безопасности
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Секретный ключ для JWT"
    )
    algorithm: str = Field(default="HS256", description="Алгоритм шифрования")
    access_token_expire_minutes: int = Field(
        default=30, 
        description="Время жизни токена в минутах"
    )
    
    # Настройки CORS
    cors_origins: Union[str, list[str]] = Field(
        default="*", 
        description="Разрешенные домены для CORS"
    )
    
    @field_validator('cors_origins')
    @classmethod
    def parse_cors_origins(cls, v):
        """Парсинг CORS origins из строки или списка."""
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Глобальный экземпляр настроек
settings = Settings()
