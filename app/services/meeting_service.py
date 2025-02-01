from abc import ABC, abstractmethod

from app.core.database import db
from app.core.enum import GoalFrequency
from app.dtos.meeting.create_meeting_dto import (
    CreateMissionMeetingDTO,
    MissionMeetingResponseDTO,
)
from app.models.meeting_model import Meeting
from app.repositories.meeting.meeting_repository import IMeetingRepository
from app.repositories.meeting.mission_meeting_repository import (
    IMissionMeetingRepository,
)


class IMeettingService(ABC):
    def __init__(
        self,
        meeting_repo: IMeetingRepository,
        mission_repo: IMissionMeetingRepository,
    ):
        self.meeting_repo = meeting_repo
        self.mission_repo = mission_repo

    @abstractmethod
    async def _create_meeting_entity_by_dto(
        self, dto: CreateMissionMeetingDTO
    ) -> Meeting:
        pass

    @abstractmethod
    async def create_mission_model(
        self, dto: CreateMissionMeetingDTO
    ) -> MissionMeetingResponseDTO:
        pass


class MeettingService(IMeettingService):
    def __init__(
        self,
        meeting_repo: IMeetingRepository,
        mission_repo: IMissionMeetingRepository,
    ):
        self.meeting_repo = meeting_repo
        self.mission_repo = mission_repo

    async def _create_meeting_entity_by_dto(
        self, dto: CreateMissionMeetingDTO
    ) -> Meeting:
        # 기본 Meeting 생성
        return Meeting(
            title=dto.title,
            description=dto.description,
            topic=dto.topic,
            place=dto.place,
            address=dto.address,
            detail_address=dto.detail_address,
            thumbnail=dto.thumbnail,
            gender_restriction=dto.conditions.gender,
            age_restriction=dto.conditions.age,
            max_participants=dto.conditions.max_participants,
        )

    @db
    async def create_mission_meeting(
        self, dto: CreateMissionMeetingDTO
    ) -> MissionMeetingResponseDTO:
        """미션 모임 생성 핵심 비즈니스 로직
        Args:
            dto: 클라이언트로부터 전달된 생성 요청 데이터 전송 객체
        Returns:
            MissionMeetingResponseDTO: 생성 결과를 포함한 응답 DTO
        Raises:
            ValueError: 필수 입력값 누락 또는 유효하지 않은 목표 주기 설정 시
        """

        # 입력 데이터 무결성 체크
        if not dto.goal_properties:
            raise ValueError("목표 속성은 필수 항목입니다")

        # 목표 주기별 필수 속성 검증
        frequency = dto.goal_properties.frequency
        if (
            frequency == GoalFrequency.WEEKLY
            and not dto.goal_properties.weekly_properties
        ):
            raise ValueError("주간 목표 속성이 필요합니다")
        if (
            frequency == GoalFrequency.MONTHLY
            and not dto.goal_properties.monthly_properties
        ):
            raise ValueError("월간 목표 속성이 필요합니다")

        # Meeting 엔티티 생성
        meeting = await self._create_meeting_entity_by_dto(dto=dto)
        meeting_entity = await self.meeting_repo.create(meeting=meeting)

        # DTO -> Mission 엔티티 변환
        # MissionMeeting 엔티티 생성
        mission_entity = dto.to_mission_entity(meeting_entity.id)
        saved_mission_entity = await self.mission_repo.create_mission(
            entity=mission_entity
        )

        # 주기별 목표 생성 전략
        weekly_goals = (
            [dto.to_weekly_goal_entity(mission_meeting_id=mission_entity)]
            if frequency == GoalFrequency.WEEKLY
            else []
        )
        monthly_goals = (
            [
                dto.to_monthly_goal_entity(None)
            ]  # None은 상위 엔티티 ID 미결정 상태 반영
            if frequency == GoalFrequency.MONTHLY
            else []
        )

        #  일괄 저장
        weekly_goal_entities, monthly_goal_entities = (
            await self.mission_repo.create_goals(
                mission_meeting_id=mission_entity.id,
                weekly_goals=weekly_goals,
                monthly_goals=monthly_goals,
            )
        )

        # 엔티티 -> 응답 DTO 변환
        return MissionMeetingResponseDTO.from_entities(
            meeting_entity,
            saved_mission_entity,
            weekly_goal_entities,
            monthly_goal_entities,
        )
