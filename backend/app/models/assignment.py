from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text
from database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, nullable=False)
    full_marks = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    file_path = Column(String, nullable=True)  # PDF/ZIP from teacher

    open_date = Column(Date, nullable=True)
    close_date = Column(Date, nullable=True)

    allow_download = Column(Boolean, default=True)