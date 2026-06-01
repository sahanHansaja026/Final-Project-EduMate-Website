from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime


class PlanEnum(str, enum.Enum):
    free = "free"
    premium = "premium"
    edu = "edu"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    user_email = Column(String, index=True)

    plan_name = Column(Enum(PlanEnum), default=PlanEnum.free)

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)

    status = Column(String, default="active")  # active / expired / cancelled