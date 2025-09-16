"""Главный роутер API v1."""

from fastapi import APIRouter

# Создание главного роутера для API v1
api_router = APIRouter()

# Здесь будут подключаться другие роутеры
# Пример:
# from app.api.v1.endpoints import users, items
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
