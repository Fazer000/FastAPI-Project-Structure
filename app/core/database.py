"""Настройка подключения к базе данных."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


# Создание движка базы данных
engine = None
async_session_maker = None

if settings.database_url:
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        future=True
    )
    async_session_maker = async_sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии базы данных."""
    if not async_session_maker:
        raise RuntimeError("Database not configured")
    
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Инициализация базы данных."""
    if not engine:
        return
    
    async with engine.begin() as conn:
        # Создание всех таблиц
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Закрытие подключения к базе данных."""
    if engine:
        await engine.dispose()
