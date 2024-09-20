from sqlalchemy.orm import Session

from app.dtos import auth
from app.repositories import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def sign_up(self, db: Session, user_info: auth.NaverUserDTO):
        # 회원정보가 존재하는지부터 확인
        is_exist = self.user_repository.user_exists_by_email(db, user_info.email)

        # 회원정보가 없으면 회원가입 시작
        if not is_exist:
            new_user = self.user_repository.sign_up(db, user_info)

            if new_user:
                return True
