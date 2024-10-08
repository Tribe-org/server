from sqlalchemy.orm import Session

from app.models import User


class AuthRepository:

    def sign_in(self, uid: str, refresh_token: str, db: Session):
        result = (
            db.query(User)
            .filter(User.uid == uid)
            .update({"refresh_token": refresh_token})
        )
        db.commit()

        return result > 0

    def sign_up(self, db: Session, user_model: User):
        """
        네이버 회원정보를 가지고 트라이브 회원으로 가입합니다.
        :return: 가입한 회원 정보
        """

        db.add(user_model)
        db.commit()

        return True

    def find_user_by_id(self, uid: str, db: Session):
        result = db.query(User).filter(User.uid == uid).first()

        return result
