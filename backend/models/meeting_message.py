from sqlalchemy import Column, String, DateTime
from database import Base
import datetime
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id = Column(String)
    sender = Column(String)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)