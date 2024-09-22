from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos import naver, user
from app.repositories import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def user_exists(self, db: Session, email: str):
        return self.user_repository.user_exists_by_email(db, email)

    def sign_up(self, db: Session, user_info: user.UserDTO):
        new_user = self.user_repository.sign_up(db, user_info)

        if not new_user:
            raise HTTPException(status_code=500, detail="회원가입에 실패했습니다.")

        return new_user
