from sqlalchemy.orm import Session

from app.repositories import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def user_exists(self, db: Session, email: str):
        return self.user_repository.user_exists_by_email(db, email)
