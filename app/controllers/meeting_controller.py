from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from app.core.route import LoggingAPIRoute

router = APIRouter(
    prefix="/meeting",
    tags=["미팅"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "서버에서 에러가 발생했습니다.",
            "content": {"application/json": {"example": {"detail": "Error Message"}}},
        },
    },
    include_in_schema=True,
    route_class=LoggingAPIRoute,
)


@router.post("")
def create_meeting():
    url = naver_service.auth_start()
    return RedirectResponse(url)
