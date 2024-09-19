from sqlalchemy.orm import Session

from ..models.badge_model import Badge
from ..schemas.badge_schema import BadgeSchema


class BadgeRepository:
    def get_all_badge(self, db: Session):
        return db.query(Badge).all()
