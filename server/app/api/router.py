from fastapi import APIRouter

from app.api.routes import assistant, avatars, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["system"])
api_router.include_router(avatars.router, prefix="/avatars", tags=["avatars"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
