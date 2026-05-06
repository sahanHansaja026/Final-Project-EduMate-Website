import uuid
from sqlalchemy import Column, String
from database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    host_id = Column(String, nullable=False)