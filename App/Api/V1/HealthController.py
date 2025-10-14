from fastapi import APIRouter, status
from datetime import datetime
from App.Core.Config import settings
from App.Core.Logger import get_logger


logger = get_logger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    """Простая проверка доступности"""
    return {"message": "pong"}

