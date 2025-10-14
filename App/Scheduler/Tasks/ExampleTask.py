from datetime import datetime
from App.Core.Logger import get_logger


logger = get_logger(__name__)


async def example_periodic_task():
    """Пример периодической задачи - выполняется каждые 30 секунд"""
    logger.info(f"[ЗАДАЧА] Выполнение периодической задачи: {datetime.utcnow().isoformat()}")
    
    # Здесь может быть любая логика
    # Например: очистка кеша, отправка уведомлений, проверка статусов и т.д.
    
    logger.info("[ЗАДАЧА] Периодическая задача завершена")


async def example_interval_task():
    """Пример задачи с интервалом - выполняется каждую минуту"""
    logger.info(f"[ЗАДАЧА] Выполнение задачи по интервалу: {datetime.utcnow().isoformat()}")
    
    # Здесь может быть логика для регулярных проверок
    
    logger.info("[ЗАДАЧА] Задача по интервалу завершена")


async def example_cron_task():
    """Пример задачи с cron расписанием - выполняется каждый час"""
    logger.info(f"[ЗАДАЧА] Выполнение cron задачи: {datetime.utcnow().isoformat()}")
    
    # Здесь может быть логика для запланированных действий
    # Например: генерация отчетов, бэкапы и т.д.
    
    logger.info("[ЗАДАЧА] Cron задача завершена")

