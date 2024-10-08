from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def user_exists_by_email(self, db: Session, email: str):
        """
        이메일을 가지고 회원 정보를 조회합니다.
        :return: 사용자 존재 여부 (True 또는 False)
        """
        return db.query(User).filter(User.email == email).count() > 0

    def sign_up(self, db: Session, user_model: User):
        """
        네이버 회원정보를 가지고 트라이브 회원으로 가입합니다.
        :return: 가입한 회원 정보
        """

        db.add(user_model)
        db.commit()

        return True
