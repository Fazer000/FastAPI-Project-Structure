from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager
from App.Core.Config import settings
from App.Core.Logger import get_logger


logger = get_logger(__name__)


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None
    _engine: Optional[AsyncEngine] = None
    _session_factory: Optional[async_sessionmaker[AsyncSession]] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            self._initialize()
    
    def _initialize(self):
        logger.info(f"Инициализация подключения к БД: {settings.database_url.split('@')[-1]}")
        
        self._engine = create_async_engine(
            settings.database_url,
            echo=settings.DATABASE_ECHO,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
        )
        
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        logger.info("База данных успешно инициализирована")
    
    @property
    def engine(self) -> AsyncEngine:
        return self._engine
    
    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
    
    async def create_tables(self):
        logger.info("Создание таблиц БД...")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы БД созданы")
    
    async def drop_tables(self):
        logger.warning("Удаление таблиц БД...")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Таблицы БД удалены")
    
    async def close(self):
        if self._engine:
            logger.info("Закрытие подключения к БД...")
            await self._engine.dispose()
            logger.info("Подключение к БД закрыто")
    
    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        session = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при работе с БД: {e}")
            raise
        finally:
            await session.close()


db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.session_scope() as session:
        yield session

