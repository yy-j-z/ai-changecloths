from fastapi import APIRouter

from app.agents.fitting_advisor import fitting_advisor
from app.schemas.assistant import AdvisorRequest, AdvisorResponse
from app.schemas.common import ApiResponse

router = APIRouter()


@router.post("/chat", response_model=ApiResponse[AdvisorResponse])
def chat_with_advisor(request: AdvisorRequest) -> ApiResponse[AdvisorResponse]:
    return ApiResponse(data=fitting_advisor.respond(request))
