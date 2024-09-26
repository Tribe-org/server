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
