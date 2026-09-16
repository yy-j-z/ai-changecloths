from fastapi import APIRouter

from app.api.routes import avatars, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["system"])
api_router.include_router(avatars.router, prefix="/avatars", tags=["avatars"])
