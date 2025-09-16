"""Middleware для приложения."""

import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования запросов."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Обработка запроса с логированием."""
        # Генерация уникального ID запроса
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Логирование начала запроса
        start_time = time.time()
        logger.info(
            f"Request started: {request.method} {request.url}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else None
            }
        )
        
        # Выполнение запроса
        try:
            response = await call_next(request)
        except Exception as exc:
            # Логирование ошибки
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url} - {str(exc)}",
                extra={
                    "request_id": request_id,
                    "process_time": process_time,
                    "error": str(exc)
                }
            )
            raise
        
        # Логирование завершения запроса
        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url} - {response.status_code}",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": process_time
            }
        )
        
        # Добавление заголовков
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware для добавления заголовков безопасности."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Добавление заголовков безопасности."""
        response = await call_next(request)
        
        # Заголовки безопасности
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response


def setup_cors_middleware(app) -> None:
    """Настройка CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_middleware(app) -> None:
    """Настройка всех middleware."""
    # Порядок важен - middleware выполняются в обратном порядке добавления
    
    # CORS (должен быть последним)
    setup_cors_middleware(app)
    
    # Заголовки безопасности
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Логирование запросов
    app.add_middleware(RequestLoggingMiddleware)
    
    logger.info("Middleware configured")
