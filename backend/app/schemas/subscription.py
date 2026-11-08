from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class PlanEnum(str, Enum):
    free = "free"
    premium = "premium"
    edu = "edu"


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    user_email: str
    plan_name: PlanEnum
    start_date: datetime
    end_date: datetime
    status: str

    class Config:
        from_attributes = True