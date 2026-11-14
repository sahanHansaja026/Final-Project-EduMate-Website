from pydantic import BaseModel
from datetime import date

class ContentResponse(BaseModel):
    assignment_id: int
    module_id: int
    title: str
    week: int
    description: str | None
    file_path: str | None
    open_date: date | None
    close_date: date | None
    allow_download: bool

    class Config:
        from_attributes = True