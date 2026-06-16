from pydantic import BaseModel, EmailStr
from datetime import datetime
from models.subscription_payment import PlanEnum


class SubscriptionPaymentResponse(BaseModel):
    id: int

    user_id: int
    user_email: EmailStr

    plan_name: PlanEnum

    start_date: datetime
    end_date: datetime

    transaction_reference: str

    receipt_file: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True