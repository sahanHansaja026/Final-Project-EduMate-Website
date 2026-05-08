from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    option_text = Column(Text, nullable=False)

    is_correct = Column(Boolean, default=False)

    question = relationship(
        "Question",
        back_populates="options"
    )