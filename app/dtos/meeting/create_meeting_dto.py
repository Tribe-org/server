from datetime import date, datetime, time

from pydantic import BaseModel, Field

from app.core.camel_model import get_camel_model_config
from app.core.enum import (
    AgeRestriction,
    CertificationType,
    GenderRestriction,
    GoalFrequency,
    MeetingPlace,
    MeetingTopic,
)
from app.models.meeting_model import Meeting
from app.models.mission_meeting_model import MissionMeeting
from app.models.mission_monthly_goal_model import MissionMonthlyGoal
from app.models.mission_weekly_goal_model import MissionWeeklyGoal


class WeeklyGoalProperties(BaseModel):
    count: int | None = Field(
        default=None, description="주/월/일 반복 횟수 (기본값: 1회)"
    )  # 주/월/일 반복 횟수 (기본값: 1회)
    day_of_week: list[int] | None = Field(
        default=None, description="요일 (1: 월요일 ~ 7: 일요일)"
    )  # 요일 (1: 월요일 ~ 7: 일요일)

    model_config = get_camel_model_config()


class MonthlyGoalProperties(BaseModel):
    day_of_month: int | None = Field(
        default=None, description="월 날짜 (1~31)"
    )  # 월 날짜 (1~31)

    model_config = get_camel_model_config()


class GoalProperties(BaseModel):
    frequency: GoalFrequency = Field(
        default=..., description="목표 주기"
    )  # 목표 주기
    start_date: datetime = Field(
        default=..., description="목표 시작 날짜"
    )  # 목표 시작 날짜
    end_date: datetime = Field(
        default=..., description="목표 종료 날짜"
    )  # 목표 종료 날짜

    weekly_properties: WeeklyGoalProperties | None = Field(
        default=None, description="주 목표 속성"
    )  # 주 목표 속성
    monthly_properties: MonthlyGoalProperties | None = Field(
        default=None, description="월 목표 속성"
    )  # 월 목표 속성

    model_config = get_camel_model_config()


class MeetingConditions(BaseModel):
    gender: GenderRestriction = Field(
        default=..., description="성별 제한"
    )  # 성별 제한
    age: AgeRestriction = Field(
        default=..., description="나이 제한"
    )  # 나이 제한

    max_participants: int = Field(
        default=..., description="참여 최대 인원(1 이상)", ge=1
    )  # 참여 최대 인원

    model_config = get_camel_model_config()


class CreateMissionMeetingDTO(BaseModel):
    topic: MeetingTopic = Field(default=..., title="모임 주제")  # 모임 주제

    place: MeetingPlace = Field(
        default=..., description="모임 장소"
    )  # 모임 장소

    address: str | None = Field(
        default=None, description="오프라인 모임 주소"
    )  # 오프라인 모임 주소
    detail_address: str | None = Field(
        default=None, description="오프라인 모임 상세 주소"
    )  # 오프라인 모임 상세 주소

    thumbnail: str | None = Field(
        default=None, description="모임 썸네일 이미지 URL"
    )  # 모임 썸네일 이미지 URL

    title: str = Field(default=..., description="모임 제목")  # 모임 제목
    description: str = Field(
        default=..., description="모임 소개글"
    )  # 모임 소개글

    goal_properties: GoalProperties = Field(
        default=None, description="목표 속성"
    )  # 목표 속성

    certification_type: CertificationType = Field(
        default=..., description="인증 유형"
    )  # 인증 유형
    certification_rule: str = Field(
        default=None, description="인증 규칙 설명"
    )  # 인증 규칙 설명

    # Conditions
    conditions: MeetingConditions = Field(
        default=..., description="모임 조건"
    )  # 모임 조건

    model_config = get_camel_model_config()

    def to_mission_entity(
        self,
        meeting_id,
    ) -> MissionMeeting:
        """순수 변환 메서드 (도메인 계층 검증 없이 기본 변환만 수행)"""
        return MissionMeeting(
            meeting_id=meeting_id,
            # 목표 관련
            start_date=self.goal_properties.start_date,
            end_date=self.goal_properties.end_date,
            goal_frequency=self.goal_properties.goal_frequency,
            # 인증 관련
            certification_type=self.certification_type,
            certification_rule=self.certification_rule,
        )

    def to_weekly_goal_entity(
        self,
        mission_meeting_id: int,
    ) -> MissionWeeklyGoal:
        """순수 변환 메서드 (도메인 계층 검증 없이 기본 변환만 수행)"""
        return MissionWeeklyGoal(
            mission_meeting_id=mission_meeting_id,
            count=self.goal_properties.weekly_properties.count,
            day_of_week=self.goal_properties.weekly_properties.day_of_week,
        )

    def to_monthly_goal_entity(
        self,
        mission_meeting_id: int,
    ) -> MissionMonthlyGoal:
        """순수 변환 메서드 (도메인 계층 검증 없이 기본 변환만 수행)"""
        return MissionMonthlyGoal(
            mission_meeting_id=mission_meeting_id,
            day_of_month=self.goal_properties.monthly_properties.day_of_month,
        )


class CreateContinuousMeetingDTO(BaseModel):
    topic: MeetingTopic = Field(
        default=..., description="모임 주제"
    )  # 모임 주제

    place: MeetingPlace = Field(
        default=..., description="모임 장소"
    )  # 모임 장소

    address: str | None = Field(
        default=None, description="오프라인 모임 주소"
    )  # 오프라인 모임 주소
    detail_address: str | None = Field(
        default=None, description="오프라인 모임 상세 주소"
    )  # 오프라인 모임 상세 주소

    thumbnail: str | None = Field(
        default=None, description="모임 썸네일 이미지 URL"
    )  # 모임 썸네일 이미지 URL

    title: str = Field(default=..., description="모임 제목")  # 모임 제목
    description: str = Field(
        default=..., description="모임 소개글"
    )  # 모임 소개글

    # Conditions
    conditions: MeetingConditions = Field(
        default=..., description="모임 조건"
    )  # 모임 조건

    offline_date: date | None = Field(
        default=None, description="오프라인 모임 날짜"
    )  # 오프라인 모임 날짜
    offline_time: time | None = Field(
        default=None, description="오프라인 모임 시간"
    )  # 오프라인 모임 시간

    model_config = get_camel_model_config()


class MissionGoalBaseResponse(BaseModel):
    id: int = Field(..., description="목표 ID")
    created_at: datetime = Field(..., description="생성 시각")

    model_config = get_camel_model_config()


class MissionWeeklyGoalResponse(MissionGoalBaseResponse):
    count: int = Field(..., description="주간 목표 횟수")
    day_of_week: list[int] = Field(..., description="요일 목록 (1-7)")

    model_config = get_camel_model_config()

    @classmethod
    def from_entity(cls, entity: MissionMeeting):
        """SQLAlchemy 엔티티를 Pydantic 모델로 변환"""
        return cls.model_validate(entity, from_attributes=True)


class MissionMonthlyGoalResponse(MissionGoalBaseResponse):
    day_of_month: int = Field(..., description="월간 목표 일자 (1-31)")

    model_config = get_camel_model_config()

    @classmethod
    def from_entity(cls, entity: MissionMeeting):
        """SQLAlchemy 엔티티를 Pydantic 모델로 변환"""
        return cls.model_validate(entity, from_attributes=True)


class MissionMeetingResponse(BaseModel):
    meeting_id: int = Field(..., description="연관된 모임 ID")
    start_date: datetime = Field(..., description="목표 시작일")
    end_date: datetime = Field(..., description="목표 종료일")
    goal_frequency: GoalFrequency = Field(..., description="목표 주기")
    certification_type: CertificationType = Field(..., description="인증 유형")
    certification_rule: str | None = Field(None, description="인증 규칙 설명")

    model_config = get_camel_model_config()

    @classmethod
    def from_entity(cls, entity: MissionMeeting):
        """SQLAlchemy 엔티티를 Pydantic 모델로 변환"""
        return cls.model_validate(entity, from_attributes=True)


class MeetingResponse(BaseModel):
    id: int = Field(..., description="모임 고유 ID")
    topic: MeetingTopic = Field(..., description="모임 주제")
    place: MeetingPlace = Field(..., description="모임 장소 유형")
    address: str | None = Field(None, description="오프라인 주소")
    detail_address: str | None = Field(None, description="오프라인 상세주소")
    thumbnail: str | None = Field(None, description="썸네일 URL")
    title: str = Field(..., description="모임 제목")
    description: str = Field(..., description="모임 상세 설명")
    conditions: MeetingConditions = Field(..., description="참여 조건")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")
    offline_date: date | None = Field(None, description="오프라인 모임 날짜")
    offline_time: time | None = Field(None, description="오프라인 모임 시간")

    model_config = get_camel_model_config()

    @classmethod
    def from_entity(cls, entity: Meeting):
        """SQLAlchemy 엔티티를 Pydantic 모델로 변환"""
        return cls.model_validate(entity, from_attributes=True)


class MissionMeetingResponseDTO(BaseModel):
    meeting: dict = Field(..., description="기본 모임 정보")
    mission: MissionMeetingResponse = Field(
        ..., description="미션 모임 상세 정보"
    )
    weekly_goals: list[MissionWeeklyGoalResponse] = Field(
        default_factory=list, description="주간 목표 리스트"
    )
    monthly_goals: list[MissionMonthlyGoalResponse] = Field(
        default_factory=list, description="월간 목표 리스트"
    )

    @classmethod
    def from_entities(
        cls,
        meeting_entity: Meeting,
        mission_entity: MissionMeeting,
        weekly_goals: list[MissionWeeklyGoal],
        monthly_goals: list[MissionMonthlyGoal],
    ) -> "MissionMeetingResponseDTO":
        """엔티티 객체로부터 DTO 생성"""
        return cls(
            meeting=MeetingResponse.from_entity(meeting_entity),
            mission=MissionMeetingResponse.from_entity(mission_entity),
            weekly_goals=[
                MissionWeeklyGoalResponse.from_entity(goal)
                for goal in weekly_goals
            ],
            monthly_goals=[
                MissionMonthlyGoalResponse.from_entity(goal)
                for goal in monthly_goals
            ],
        )

    model_config = get_camel_model_config()
