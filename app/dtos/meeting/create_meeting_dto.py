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
