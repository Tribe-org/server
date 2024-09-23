from app.schemas import UserSchema


class UserDTO(UserSchema):
    class Config:
        from_attributes = True
