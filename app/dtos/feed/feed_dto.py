from pydantic import BaseModel

class FeedDTO(BaseModel):
    id: int
    content: str
    type: str

    class Config:
        use_enum_values = True
