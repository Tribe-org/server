from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Database
from app.models.mission_meeting_model import MissionMeeting


class MissionWeeklyGoal(Database.base):
    __tablename__ = "mission_weekly_goals"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    mission_meeting_id: Mapped[int] = mapped_column(
        ForeignKey("mission_meetings.id"), nullable=False
    )
    mission_meeting: Mapped[MissionMeeting] = relationship(
        back_populates="weekly_goals"
    )

    count: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # 1-7 (월-일)
