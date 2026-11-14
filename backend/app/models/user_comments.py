from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class UserComment(Base):
    __tablename__ = "user_comments"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    rating = Column(Integer)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    module = relationship("Module", back_populates="user_comments")
    user = relationship("User", back_populates="user_comments")