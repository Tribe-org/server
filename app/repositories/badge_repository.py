from sqlalchemy.orm import Session

from ..models.badge_model import Badge


class BadgeRepository:
    def get_all_badge(self, db: Session):
        return db.query(Badge).all()
