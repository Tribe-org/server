from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, Form, status, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import Body

from app.core.di_container import Container
from app.core.route import LoggingAPIRoute
from app.dtos.meeting.create_meeting_dto import (
    CreateMissionMeetingDTO,
    MissionMeetingResponseDTO,
)
from app.services.meeting_service import MeettingService
from app.core.supabase import Supabase

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
    path="/image/upload",
    summary="미팅 이미지 업로드",
    status_code=status.HTTP_201_CREATED,
)
async def create_meeting_image(
    meeting_service: MeettingService = Depends(
        Provide[Container.meeting_service]
    ),
    image: UploadFile = Form(..., media_type="multipart/form-data"),
):
    # 현재 시간을 기반으로 유니크한 파일 경로 생성
    now = datetime.now()
    file_path = f"tmp/{now.strftime('%Y%m%d_%H%M%S_%f')}{image.filename}"
    
    # 이미지 데이터 읽기
    image_data = await image.read()
    
    # Supabase storage에 업로드
    supabase = Supabase()
    response = supabase.storage.from_('bucket_name').upload(
        file_path,
        image_data,
        {'upsert': 'true'}
    )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"file_path": file_path}
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
