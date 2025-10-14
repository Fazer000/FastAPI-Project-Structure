from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from App.Core.Config import settings
from App.Core.Logger import logger
from App.Core.Database import db_manager
from App.Scheduler.SchedulerManager import scheduler_manager
from App.Scheduler.TaskRegistry import register_all_tasks
from App.Api.V1.Router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    logger.info("=" * 60)
    logger.info(f"Запуск приложения: {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 60)
    
    # Инициализация БД
    logger.info("Проверка подключения к БД...")
    try:
        async with db_manager.session_scope() as session:
            await session.execute("SELECT 1")
        logger.info("✓ Подключение к БД установлено")
    except Exception as e:
        logger.error(f"✗ Ошибка подключения к БД: {e}")
        raise
    
    # Запуск планировщика
    if settings.SCHEDULER_ENABLED:
        register_all_tasks()
        scheduler_manager.start()
        logger.info("✓ Планировщик задач запущен")
    
    logger.info("=" * 60)
    logger.info(f"Приложение готово к работе на {settings.HOST}:{settings.PORT}")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("Остановка приложения...")
    logger.info("=" * 60)
    
    # Остановка планировщика
    if settings.SCHEDULER_ENABLED:
        scheduler_manager.shutdown()
        logger.info("✓ Планировщик задач остановлен")
    
    # Закрытие БД
    await db_manager.close()
    logger.info("✓ Подключение к БД закрыто")
    
    logger.info("=" * 60)
    logger.info("Приложение остановлено")
    logger.info("=" * 60)


class Application:
    def __init__(self):
        self.app = FastAPI(
            title=settings.APP_NAME,
            version=settings.APP_VERSION,
            debug=settings.DEBUG,
            lifespan=lifespan,
            docs_url=None,
            redoc_url=None
        )
        
        self._setup_middleware()
        self._setup_routes()
        self._setup_scalar()
    
    def _setup_middleware(self):
        """Настройка middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_CREDENTIALS,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
        )
        logger.info("✓ CORS middleware настроен")
    
    def _setup_routes(self):
        """Настройка роутов"""
        self.app.include_router(api_v1_router)
        logger.info("✓ API роуты зарегистрированы")
    
    def _setup_scalar(self):
        """Настройка Scalar документации"""
        @self.app.get("/docs", include_in_schema=False)
        async def scalar_html():
            return get_scalar_api_reference(
                openapi_url=self.app.openapi_url,
                title=f"{settings.APP_NAME} - API Documentation",
            )
        logger.info("✓ Scalar документация настроена")
    
    def get_app(self) -> FastAPI:
        return self.app


def create_app() -> FastAPI:
    """Фабрика для создания приложения"""
    application = Application()
    return application.get_app()


app = create_app()

