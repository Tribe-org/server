from abc import ABC, abstractmethod
from typing import Tuple

from sqlalchemy.orm import Session

from app.core.database import db
from app.models import MissionMonthlyGoal, MissionWeeklyGoal
from app.models.mission_meeting_model import MissionMeeting


class IMissionMeetingRepository(ABC):
    @abstractmethod
    async def create_mission(
        self, entity: MissionMeeting, db: Session
    ) -> MissionMeeting:
        pass

    @abstractmethod
    async def create_goals(
        self,
        mission_meeting_id: int,
        db: Session,
        weekly_goals=[],
        monthly_goals=[],
    ) -> Tuple[MissionWeeklyGoal, MissionMonthlyGoal]:
        pass

    @abstractmethod
    async def get_goals(
        self,
        mission_id: int,
        db: Session,
    ):
        pass


class MissionMeetingRepository(IMissionMeetingRepository):
    def __init__(self):
        pass

    @db
    async def create_mission(
        self, db: Session, entity: MissionMeeting
    ) -> MissionMeeting:
        db.add(entity)
        db.flush(entity)  # ID를 얻기 위해 flush
        return entity

    @db
    async def create_goals(
        self,
        db: Session,
        mission_meeting_id: int,
        weekly_goals=[],
        monthly_goals=[],
    ) -> Tuple[MissionWeeklyGoal, MissionMonthlyGoal]:
        weekly_goal_entities = []
        # 주간 목표 일괄 생성
        for goal in weekly_goals:
            goal_obj = MissionWeeklyGoal(
                mission_meeting_id=mission_meeting_id, **goal.dict()
            )
            db.add(goal_obj)
            weekly_goal_entities.append(goal_obj)

        monthly_goal_entities = []
        # 월간 목표 일괄 생성
        for goal in monthly_goals:
            goal_obj = MissionMonthlyGoal(
                mission_meeting_id=mission_meeting_id, **goal.dict()
            )
            db.add(goal_obj)
            monthly_goal_entities.append(goal_obj)

        return weekly_goal_entities, monthly_goal_entities

    @db
    async def get_goals(self, db: Session, mission_id: int):
        return {
            "weekly": db.query(MissionWeeklyGoal)
            .filter_by(mission_meeting_id=mission_id)
            .all(),
            "monthly": db.query(MissionMonthlyGoal)
            .filter_by(mission_meeting_id=mission_id)
            .all(),
        }
