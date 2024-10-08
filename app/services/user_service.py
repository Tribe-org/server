from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos import naver, user
from app.enums import GenderType
from app.models import User
from app.repositories import UserRepository
from app.utils import create_timestamptz


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def user_exists(self, db: Session, email: str):
        return self.user_repository.user_exists_by_email(db, email)
