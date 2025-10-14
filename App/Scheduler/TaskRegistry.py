from App.Scheduler.SchedulerManager import scheduler_manager
from App.Scheduler.Tasks.ExampleTask import (
    example_periodic_task,
    example_interval_task,
    example_cron_task
)
from App.Core.Logger import get_logger


logger = get_logger(__name__)


def register_all_tasks():
    """Регистрация всех задач в планировщике"""
    logger.info("Регистрация задач в планировщике...")
    
    # Пример 1: Задача каждые 30 секунд
    scheduler_manager.add_job(
        func=example_periodic_task,
        trigger='interval',
        id='example_periodic_task',
        name='Периодическая задача (каждые 30 сек)',
        seconds=30
    )
    
    # Пример 2: Задача каждую минуту
    scheduler_manager.add_job(
        func=example_interval_task,
        trigger='interval',
        id='example_interval_task',
        name='Задача по интервалу (каждую минуту)',
        minutes=1
    )
    
    # Пример 3: Задача по cron расписанию (каждый час)
    scheduler_manager.add_job(
        func=example_cron_task,
        trigger='cron',
        id='example_cron_task',
        name='Cron задача (каждый час)',
        hour='*',
        minute=0
    )
    
    logger.info(f"Зарегистрировано задач: {len(scheduler_manager.get_jobs())}")


def unregister_all_tasks():
    """Отмена регистрации всех задач"""
    logger.info("Отмена регистрации задач...")
    for job in scheduler_manager.get_jobs():
        scheduler_manager.remove_job(job.id)
    logger.info("Все задачи отменены")

