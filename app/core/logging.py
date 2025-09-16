"""Настройка логирования."""

import logging
import sys
from typing import Dict, Any
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    """Настройка системы логирования."""
    
    # Создание директории для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Настройка форматирования
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Базовая конфигурация
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Консольный вывод
            logging.StreamHandler(sys.stdout),
            # Файловый вывод
            logging.FileHandler(
                log_dir / "app.log",
                mode="a",
                encoding="utf-8"
            )
        ]
    )
    
    # Настройка уровней для внешних библиотек
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.debug else logging.WARNING
    )
    
    # Создание логгера приложения
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    app_logger.info("Logging system initialized")


def get_logger(name: str) -> logging.Logger:
    """Получение логгера по имени."""
    return logging.getLogger(f"app.{name}")


class LoggerMixin:
    """Миксин для добавления логгера в классы."""
    
    @property
    def logger(self) -> logging.Logger:
        """Логгер для текущего класса."""
        return get_logger(self.__class__.__name__)


def log_request_info(request_data: Dict[str, Any]) -> None:
    """Логирование информации о запросе."""
    logger = get_logger("requests")
    logger.info(
        f"Request: {request_data.get('method')} {request_data.get('url')}",
        extra={"request_data": request_data}
    )


def log_response_info(response_data: Dict[str, Any]) -> None:
    """Логирование информации об ответе."""
    logger = get_logger("responses")
    logger.info(
        f"Response: {response_data.get('status_code')}",
        extra={"response_data": response_data}
    )
