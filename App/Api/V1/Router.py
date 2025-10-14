from fastapi import APIRouter
from App.Api.V1.HealthController import router as health_router
from App.Api.V1.UserController import router as user_router


api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(user_router)

