from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Database
from app.models.mission_meeting_model import MissionMeeting


class MissionMonthlyGoal(Database.base):
    __tablename__ = "mission_monthly_goals"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    mission_meeting_id: Mapped[int] = mapped_column(
        ForeignKey("mission_meetings.id"), nullable=False
    )
    mission_meeting: Mapped[MissionMeeting] = relationship(
        back_populates="monthly_goals"
    )

    day_of_month: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-31
