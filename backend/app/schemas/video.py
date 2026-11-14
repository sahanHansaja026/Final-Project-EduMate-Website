from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class VideoResponse(BaseModel):
    id: int
    module_id: int

    title: str
    description: Optional[str]

    source_type: str

    video_url: Optional[str]
    thumbnail_url: Optional[str]

    open_date: Optional[date]
    close_date: Optional[date]

    created_at: datetime

    class Config:
        from_attributes = True