from sqlalchemy.orm import Session

from app.models import Badge


class BadgeRepository:
    def get_all_badge(self, db: Session):
        return db.query(Badge).all()
