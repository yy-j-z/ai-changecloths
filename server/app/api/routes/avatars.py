from fastapi import APIRouter

from app.schemas.avatar import AvatarConfig
from app.schemas.common import ApiResponse

router = APIRouter()


@router.get("/defaults", response_model=ApiResponse[AvatarConfig])
def avatar_defaults() -> ApiResponse[AvatarConfig]:
    """Return the canonical avatar parameter contract used by the web client."""
    return ApiResponse(data=AvatarConfig())
