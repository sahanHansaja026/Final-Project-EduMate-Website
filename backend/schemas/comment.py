from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    user_id: int
    module_id: int
    text: str


class CommentResponse(BaseModel):
    id: int
    user_id: int
    module_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    text: str