"""FastAPI зависимости."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import UnauthorizedException


# Схема безопасности для JWT
security = HTTPBearer(auto_error=False)


async def get_db() -> AsyncSession:
    """Зависимость для получения сессии базы данных."""
    async for session in get_async_session():
        yield session


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Зависимость для получения текущего пользователя."""
    if not credentials:
        raise UnauthorizedException("Authorization header required")
    
    # Здесь будет логика проверки JWT токена
    # Пока возвращаем заглушку
    return {"user_id": 1, "username": "test_user"}


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    """Зависимость для получения активного пользователя."""
    # Здесь можно добавить проверку активности пользователя
    return current_user


class CommonQueryParams:
    """Общие параметры запроса для пагинации и сортировки."""
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ):
        self.skip = skip
        self.limit = min(limit, 1000)  # Максимум 1000 записей
        self.order_by = order_by
        self.order_desc = order_desc
