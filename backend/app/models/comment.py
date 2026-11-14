from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from database import Base


class Comment(Base):
    __tablename__ = "user_comments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)
    module_id = Column(Integer, nullable=False,index=True)

    text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())