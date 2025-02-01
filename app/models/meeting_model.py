from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Database
from app.core.enum import (
    AgeRestriction,
    GenderRestriction,
    MeetingPlace,
    MeetingTopic,
)
from app.models.mission_meeting_model import MissionMeeting


class Meeting(Database.Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)

    topic: Mapped[MeetingTopic] = mapped_column(
        Enum(MeetingTopic), nullable=False
    )
    place: Mapped[MeetingPlace] = mapped_column(
        Enum(MeetingPlace), nullable=False
    )

    address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    detail_address: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )
    thumbnail: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )  # noqa

    # 모임 조건
    gender_restriction: Mapped[GenderRestriction] = mapped_column(
        Enum(GenderRestriction), nullable=False
    )
    age_restriction: Mapped[AgeRestriction] = mapped_column(
        Enum(AgeRestriction), nullable=False
    )
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)

    # 관계
    mission_meeting: Mapped["MissionMeeting"] = relationship(
        back_populates="meeting", uselist=False
    )
    created_at = mapped_column(
        DateTime, nullable=False, default=datetime.now(UTC)
    )
    updated_at = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
    deleted_at = mapped_column(DateTime, nullable=True)
