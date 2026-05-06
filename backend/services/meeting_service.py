from models.meeting import Meeting
from database import SessionLocal

db = SessionLocal()

def create_meeting(data):
    meeting = Meeting(
        title=data.title,
        host_id=data.host_id
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


def get_meeting(meeting_id):
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()