from pydantic import BaseModel
from datetime import date
from typing import Optional

class AssignmentResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: Optional[str]
    file_path: Optional[str]
    open_date: Optional[date]
    close_date: Optional[date]
    allow_download: bool

    class Config:
        from_attributes = True