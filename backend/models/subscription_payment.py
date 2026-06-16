from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
from datetime import datetime
import enum


class PlanEnum(str, enum.Enum):
    free = "free"
    premium = "premium"
    edu = "edu"


class SubscriptionPayment(Base):
    __tablename__ = "subscription_payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)
    user_email = Column(String, index=True, nullable=False)

    plan_name = Column(Enum(PlanEnum), nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    transaction_reference = Column(String, nullable=False)

    receipt_file = Column(String, nullable=False)

    status = Column(String, default="pending", nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)