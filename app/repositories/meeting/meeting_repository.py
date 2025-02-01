from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.database import db
from app.models.meeting_model import Meeting


class MeetingRepository:
    def __init__(self):
        pass

    @db
    def create(self, db: Session, meeting: Meeting):
        db.add(meeting)
        db.refresh(meeting)
        return meeting

    @db
    def get_by_id(self, db: Session, meeting_id: int) -> Meeting | None:
        return db.query(Meeting).filter(Meeting.id == meeting_id).first()

    @db
    def update(self, db: Session, meeting_id: int, meeting_data):
        meeting = self.get_by_id(meeting_id)
        if meeting:
            for key, value in meeting_data.dict().items():
                setattr(meeting, key, value)

            db.refresh(meeting)
        return meeting

    @db
    def delete(self, db: Session, meeting_id: int):
        meeting = self.get_by_id(meeting_id)
        if meeting:
            meeting.deleted_at = datetime.now(UTC)
            db.delete(meeting)

        return meeting

    @db
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Meeting).offset(skip).limit(limit).all()
