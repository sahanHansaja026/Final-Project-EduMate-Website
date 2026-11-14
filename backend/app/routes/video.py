from fastapi import APIRouter, Depends, HTTPException, status, Form, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.video import Video
from app.schemas.video import VideoResponse

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/", response_model=VideoResponse, status_code=201)
def create_video(
    title: str = Form(...),
    module_id: int = Form(...),
    url: str = Form(...),
    db: Session = Depends(get_db),
):
    from app.models.module import Module
    # Validate module exists
    module = db.query(Module).filter(Module.module_id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    new_video = Video(
        title=title,
        module_id=module_id,
        url=url,
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return VideoResponse.from_orm(new_video)

@router.get("/module/{module_id}", response_model=list[VideoResponse])
def get_videos_by_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.video import Video
    videos = db.query(Video).filter(Video.module_id == module_id).all()
    return [VideoResponse.from_orm(v) for v in videos]

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(Video.video_id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return VideoResponse.from_orm(video)