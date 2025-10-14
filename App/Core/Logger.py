import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
from App.Core.Config import settings


class LoggerManager:
    _instance: Optional['LoggerManager'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        self._logger = logging.getLogger(settings.APP_NAME)
        self._logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
        
        # Удаляем существующие обработчики
        self._logger.handlers.clear()
        
        # Форматтер
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Консольный обработчик
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # Файловый обработчик
        log_file = Path(settings.LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
    
    @property
    def logger(self) -> logging.Logger:
        return self._logger
    
    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(f"{settings.APP_NAME}.{name}")


logger_manager = LoggerManager()
logger = logger_manager.logger


def get_logger(name: str) -> logging.Logger:
    return logger_manager.get_logger(name)

