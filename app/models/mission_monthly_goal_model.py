from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Database


class MissionMonthlyGoal(Database.Base):
    __tablename__ = "mission_monthly_goals"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    mission_meeting_id: Mapped[int] = mapped_column(
        ForeignKey("mission_meetings.id"), nullable=False
    )

    day_of_month: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-31
