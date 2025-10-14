from typing import Optional, Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from pytz import timezone
from App.Core.Config import settings
from App.Core.Logger import get_logger


logger = get_logger(__name__)


class SchedulerManager:
    _instance: Optional['SchedulerManager'] = None
    _scheduler: Optional[AsyncIOScheduler] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._scheduler is None and settings.SCHEDULER_ENABLED:
            self._initialize_scheduler()
    
    def _initialize_scheduler(self):
        logger.info("Инициализация планировщика задач...")
        
        jobstores = {
            'default': MemoryJobStore()
        }
        
        executors = {
            'default': AsyncIOExecutor()
        }
        
        job_defaults = {
            'coalesce': False,
            'max_instances': 3,
            'misfire_grace_time': 60
        }
        
        self._scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=timezone(settings.SCHEDULER_TIMEZONE)
        )
        
        logger.info("Планировщик задач инициализирован")
    
    @property
    def scheduler(self) -> Optional[AsyncIOScheduler]:
        return self._scheduler
    
    def add_job(
        self,
        func: Callable,
        trigger: str,
        id: str,
        name: str = None,
        replace_existing: bool = True,
        **trigger_args
    ):
        if not self._scheduler:
            logger.warning("Планировщик не инициализирован")
            return
        
        logger.info(f"Добавление задачи: {id} ({name or id})")
        
        self._scheduler.add_job(
            func=func,
            trigger=trigger,
            id=id,
            name=name or id,
            replace_existing=replace_existing,
            **trigger_args
        )
    
    def remove_job(self, job_id: str):
        if not self._scheduler:
            return
        
        logger.info(f"Удаление задачи: {job_id}")
        self._scheduler.remove_job(job_id)
    
    def start(self):
        if not self._scheduler:
            logger.warning("Планировщик не инициализирован")
            return
        
        logger.info("Запуск планировщика задач...")
        self._scheduler.start()
        logger.info("Планировщик задач запущен")
    
    def shutdown(self, wait: bool = True):
        if not self._scheduler:
            return
        
        logger.info("Остановка планировщика задач...")
        self._scheduler.shutdown(wait=wait)
        logger.info("Планировщик задач остановлен")
    
    def get_jobs(self):
        if not self._scheduler:
            return []
        return self._scheduler.get_jobs()


scheduler_manager = SchedulerManager()

