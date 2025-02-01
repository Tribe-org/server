from abc import ABC, abstractmethod
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.database import db
from app.models.meeting_model import Meeting


class IMeetingRepository(ABC):
    @abstractmethod
    async def create(self, db: Session, meeting: Meeting):
        pass

    @abstractmethod
    async def get_by_id(self, db: Session, meeting_id: int) -> Meeting | None:
        pass

    @abstractmethod
    async def update(self, db: Session, meeting_id: int, meeting_data):
        pass

    @abstractmethod
    async def delete(self, db: Session, meeting_id: int):
        pass

    @abstractmethod
    async def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        pass


class MeetingRepository(IMeetingRepository):
    def __init__(self):
        pass

    @db
    async def create(self, db: Session, meeting: Meeting):
        db.add(meeting)
        db.refresh(meeting)
        return meeting

    @db
    async def get_by_id(self, db: Session, meeting_id: int) -> Meeting | None:
        return db.query(Meeting).filter(Meeting.id == meeting_id).first()

    @db
    async def update(self, db: Session, meeting_id: int, meeting_data):
        meeting = self.get_by_id(meeting_id)
        if meeting:
            for key, value in meeting_data.dict().items():
                setattr(meeting, key, value)

            db.refresh(meeting)
        return meeting

    @db
    async def delete(self, db: Session, meeting_id: int):
        meeting = self.get_by_id(meeting_id)
        if meeting:
            meeting.deleted_at = datetime.now(UTC)
            db.delete(meeting)

        return meeting

    @db
    async def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Meeting).offset(skip).limit(limit).all()
