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
        # 입력 유효성 검증
        if not dto.goal_properties:
            raise ValueError("목표 속성은 필수 항목입니다")

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

        # 기본 Meeting 생성
        meeting = await self._create_meeting_entity_by_dto(dto=dto)
        meeting_entity = await self.meeting_repo.create(meeting=meeting)

        # Mission Meeting 엔티티 변환
        mission_entity = dto.to_mission_entity(meeting_entity.id)
        saved_mission_entity = await self.mission_repo.create_mission(
            entity=mission_entity
        )

        # 주기별 목표 생성
        weekly_goals = (
            [dto.to_weekly_goal_entity(mission_meeting_id=mission_entity)]
            if frequency == GoalFrequency.WEEKLY
            else []
        )
        monthly_goals = (
            [dto.to_monthly_goal_entity(None)]
            if frequency == GoalFrequency.MONTHLY
            else []
        )

        # 트랜잭션 내 저장
        weekly_goal_entities, monthly_goal_entities = (
            await self.mission_repo.create_goals(
                mission_meeting_id=mission_entity.id,
                weekly_goals=weekly_goals,
                monthly_goals=monthly_goals,
            )
        )

        return MissionMeetingResponseDTO.from_entities(
            meeting_entity,
            saved_mission_entity,
            weekly_goal_entities,
            monthly_goal_entities,
        )
