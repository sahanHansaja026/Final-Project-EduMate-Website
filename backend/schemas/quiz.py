from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class QuizBase(BaseModel):
    module_id: int
    title: str
    description: Optional[str] = None

    attempts: Optional[str] = "unlimited"

    open_date: Optional[datetime] = None
    close_date: Optional[datetime] = None

    is_graded: Optional[bool] = True
    shuffle_questions: Optional[bool] = False


class QuizResponse(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)