from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def user_exists_by_email(self, db: Session, email: str):
        """
        이메일을 가지고 회원 정보를 조회합니다.
        :return: 사용자 존재 여부 (True 또는 False)
        """
        return db.query(User).filter(User.email == email).count() > 0
