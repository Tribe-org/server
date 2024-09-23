from pydantic import BaseModel

from app.schemas import NaverUserSchema


class NaverUserDTO(NaverUserSchema):
    class Config:
        use_enum_values = True


class NaverUserInfoWithCodeDTO(BaseModel):
    code: str


class NaverUserInfoWithEmailAndNameDTO(BaseModel):
    email: str
    name: str
