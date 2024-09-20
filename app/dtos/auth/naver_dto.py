from typing import Optional

from pydantic import BaseModel

from app.enums import GenderType


class NaverUserDTO(BaseModel):
    id: str
    age: Optional[str] = None
    gender: GenderType = GenderType.U
    email: str
    name: str

    class Config:
        use_enum_values = True
