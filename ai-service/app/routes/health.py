from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, object]:
    return {"code": 0, "message": "ok", "data": {"service": "ai", "status": "alive"}}
