from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from database import Base

class ModuleQuizAccessController(Base):
    __tablename__ = "module_quiz_access_controller"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    granted_at = Column(DateTime, default=datetime.utcnow)

    module = relationship("Module", back_populates="quiz_access_controllers")
    quiz = relationship("Quiz", back_populates="module_access_controllers")
    user = relationship("User", back_populates="module_access_controllers")