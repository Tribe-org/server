from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Database
from app.models.mission_monthly_goal_model import MissionMonthlyGoal
from app.models.mission_weekly_goal_model import MissionWeeklyGoal


class MissionMeeting(Database.Base):
    __tablename__ = "mission_meetings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"), nullable=False
    )

    # 목표 관련
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    goal_frequency: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # DAILY, WEEKLY, MONTHLY

    # 인증 관련
    certification_type: Mapped[str] = mapped_column(String(50), nullable=False)
    certification_rule: Mapped[str] = mapped_column(
        String(500), nullable=False
    )  # noqa

    # 주간/월간 목표 속성은 별도 테이블로 관리 가능
    weekly_goals: Mapped[list["MissionWeeklyGoal"]] = relationship(
        back_populates="mission_meeting"
    )
    monthly_goals: Mapped[list["MissionMonthlyGoal"]] = relationship(
        back_populates="mission_meeting"
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
