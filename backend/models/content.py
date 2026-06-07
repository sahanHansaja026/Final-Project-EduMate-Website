from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from database import Base

class Content(Base):
    __tablename__ = "module_contents"

    assignment_id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, nullable=False)

    title = Column(String, nullable=False)
    week = Column(Integer, nullable=False)
    description = Column(String)

    file_path = Column(String)  # ✅ store file path instead of bytes

    open_date = Column(Date)
    close_date = Column(Date)

    allow_download = Column(Boolean, default=True)