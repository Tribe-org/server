from sqlalchemy.orm import Session

from app.core.database import db


class MeettingService:
    def __init__(self):
        pass

    @db
    def user_exists(self, db: Session, email: str):
        pass
