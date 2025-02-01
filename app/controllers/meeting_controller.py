from dependency_injector.wiring import Provide
from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.di_container import Container
from app.core.route import LoggingAPIRoute
from app.dtos.meeting.create_meeting_dto import (
    CreateMissionMeetingDTO,
    MissionMeetingResponseDTO,
)
from app.services.meeting_service import MeettingService

router = APIRouter(
    prefix="/v1/meeting",
    tags=["미팅"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "서버에서 에러가 발생했습니다.",
            "content": {
                "application/json": {"example": {"detail": "Error Message"}}
            },
        },
    },
    include_in_schema=True,
    route_class=LoggingAPIRoute,
)


@router.post(
    path="/mission",
    summary="미션 모임 생성",
    status_code=status.HTTP_201_CREATED,
    response_model=MissionMeetingResponseDTO,
)
async def create_mission_meeting(
    meeting_service: MeettingService = Depends(
        Provide[Container.meeting_service]
    ),
    dto: CreateMissionMeetingDTO = Body(...),
):
    response: MissionMeetingResponseDTO = (
        await meeting_service.create_mission_meeting(dto=dto)
    )

    return JSONResponse(
        content=jsonable_encoder(response), status_code=status.HTTP_201_CREATED
    )
