from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.core.database import db
from app.models.meeting_model import ContinuousMeeting


class IContinuousMeetingRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_with_continuous(
        self, db: Session, meeting_data, continuous_data
    ):
        pass


class ContinuousMeetingRepository(IContinuousMeetingRepository):
    def __init__(self):
        pass

    @db
    def create_with_continuous(
        self, db: Session, meeting_id: int, continuous_data
    ):

        continuous = ContinuousMeeting(
            meeting_id=meeting_id, **continuous_data.dict()
        )
        db.add(continuous)
        return None
