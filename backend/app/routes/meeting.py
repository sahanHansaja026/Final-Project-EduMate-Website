from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.meeting import Meeting

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.post("/", response_model=dict, status_code=201)
def create_meeting(
    title: str,
    description: str = None,
    module_id: int = None,
    db: Session = Depends(get_db),
):
    from app.models.module import Module
    # Validate module if provided
    if module_id:
        module = db.query(Module).filter(Module.module_id == module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

    new_meeting = Meeting(
        title=title,
        description=description,
        module_id=module_id,
    )
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return {"message": "Meeting created", "meeting_id": new_meeting.meeting_id}

@router.get("/", response_model=list)
def get_meetings(
    db: Session = Depends(get_db),
    module_id: int = None,
):
    query = db.query(Meeting)
    if module_id:
        query = query.filter(Meeting.module_id == module_id)
    return query.all()

@router.get("/{meeting_id}", response_model=dict)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {
        "meeting_id": meeting.meeting_id,
        "title": meeting.title,
        "description": meeting.description,
        "module_id": meeting.module_id,
    }