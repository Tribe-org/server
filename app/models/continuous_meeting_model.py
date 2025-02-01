from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Database
from app.models.meeting_model import Meeting


class ContinuousMeeting(Database.base):
    __tablename__ = "continuous_meetings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"), nullable=False
    )
    meeting: Mapped[Meeting] = relationship(
        back_populates="continuous_meeting"
    )  # noqa

    offline_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    offline_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
