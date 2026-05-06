import os
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.meeting import Meeting
from schemas.meeting import MeetingCreate, MeetingResponse

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.post("/", response_model=MeetingResponse)
def create_meeting(
    data: MeetingCreate,
    db: Session = Depends(get_db)
):
    meeting = Meeting(
        title=data.title,
        host_id=data.host_id
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting
# get all meetings
@router.get("/", response_model=List[MeetingResponse])
def get_meetings(db: Session = Depends(get_db)):
    return db.query(Meeting).all()

# get single meeting
@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return meeting
# delete meeting
@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    db.delete(meeting)
    db.commit()

    return {"message": "Meeting deleted"}