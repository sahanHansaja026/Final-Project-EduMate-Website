from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.video_access_control import VideoAccessControl

router = APIRouter(prefix="/video-access-control", tags=["VideoAccessControl"])

@router.post("/create", response_model=dict)
def create_video_access(
    video_id: int,
    user_id: int,
    plan_type: str,
    db: Session = Depends(get_db),
):
    from app.models.video_access_control import VideoAccessControl
    new_access = VideoAccessControl(
        video_id=video_id,
        user_id=user_id,
        plan_type=plan_type,
    )
    db.add(new_access)
    db.commit()
    db.refresh(new_access)
    return {"message": "Video access control created", "access_id": new_access.access_id}

@router.get("/video/{video_id}/user/{user_id}", response_model=bool)
def check_video_access(
    video_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.video_access_control import VideoAccessControl
    access = db.query(VideoAccessControl).filter(
        VideoAccessControl.video_id == video_id,
        VideoAccessControl.user_id == user_id
    ).first()
    return {"has_access": access is not None}

@router.get("/", response_model=list)
def get_video_access_by_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    from app.models.video_access_control import VideoAccessControl
    accesses = db.query(VideoAccessControl).filter(VideoAccessControl.video_id == video_id).all()
    return [{"user_id": a.user_id, "plan_type": a.plan_type} for a in accesses]