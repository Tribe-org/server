from sqlalchemy.orm import Session

from ..repositories.badge_repository import BadgeRepository


class BadgeService:
    def __init__(self) -> None:
        self.badge_repository = BadgeRepository()

    def get_all_badge(self, db: Session):
        return self.badge_repository.get_all_badge(db)
