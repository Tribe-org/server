from typing import Optional

from pydantic import BaseModel

from app.enums import GenderType


class NaverUserSchema(BaseModel):
    id: str
    email: str
    name: str
    birthday: str
    birthyear: int
    gender: GenderType
    age: Optional[str] = None

    class Config:
        use_enum_values = True
