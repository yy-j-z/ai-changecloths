from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.size_recommendation import recommend_size

router = APIRouter()


class SizeRequest(BaseModel):
    height_cm: float = Field(gt=80, lt=250)
    weight_kg: float = Field(gt=20, lt=300)


class SizeResult(BaseModel):
    size: str
    fit: str
    basis: str


@router.post("/recommend")
def size_recommendation(request: SizeRequest) -> dict[str, object]:
    size = recommend_size(request.height_cm, request.weight_kg)
    result = SizeResult(size=size, fit="regular", basis="demo BMI rule")
    return {"code": 0, "message": "ok", "data": result.model_dump()}
