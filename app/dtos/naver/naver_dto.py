from pydantic import BaseModel


class NaverUserInfoWithEmailAndNameDTO(BaseModel):
    email: str
    name: str


class NaverUserInfoWithCodeDTO(BaseModel):
    code: str
