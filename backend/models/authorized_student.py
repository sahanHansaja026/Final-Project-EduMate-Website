from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from database import Base


class AuthorizedStudent(Base):
    __tablename__ = "authorized_students"

    id = Column(Integer, primary_key=True, index=True)

    channel_module_id = Column(Integer, nullable=False)  # just store id, no FK

    student_name = Column(String(255), nullable=False)

    student_email = Column(String(255), nullable=False)

    admission_date = Column(
        DateTime,
        server_default=func.now()
    )

    status = Column(String(20), default="active")  # active | suspend

    remark = Column(Text, nullable=True)