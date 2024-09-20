from pydantic import BaseModel


class NaverUserInfoDTO(BaseModel):
    email: str
    name: str
