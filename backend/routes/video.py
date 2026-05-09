import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from database import get_db
from models.video import Video
from schemas.video import VideoResponse


router = APIRouter(prefix="/videos", tags=["Videos"])


# =========================
# FOLDERS
# =========================

VIDEO_DIR = "uploads/videos"
THUMBNAIL_DIR = "uploads/thumbnails"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)


# =========================
# CREATE VIDEO
# =========================

@router.post("/", response_model=VideoResponse)
async def create_video(
    module_id: int = Form(...),

    title: str = Form(...),
    description: Optional[str] = Form(None),

    source_type: str = Form(...),

    video_url: Optional[str] = Form(None),

    video_file: UploadFile = File(None),
    thumbnail: UploadFile = File(None),

    open_date: Optional[date] = Form(None),
    close_date: Optional[date] = Form(None),

    db: Session = Depends(get_db),
):

    saved_video_path = None
    saved_thumbnail_path = None

    # =========================
    # SAVE VIDEO FILE
    # =========================

    if source_type == "Upload":

        if not video_file:
            raise HTTPException(
                status_code=400,
                detail="Video file is required"
            )

        video_path = f"{VIDEO_DIR}/{video_file.filename}"

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)

        saved_video_path = video_path

    else:
        saved_video_path = video_url

    # =========================
    # SAVE THUMBNAIL
    # =========================

    if thumbnail:

        thumb_path = f"{THUMBNAIL_DIR}/{thumbnail.filename}"

        with open(thumb_path, "wb") as buffer:
            shutil.copyfileobj(thumbnail.file, buffer)

        saved_thumbnail_path = thumb_path

    # =========================
    # SAVE DB
    # =========================

    new_video = Video(
        module_id=module_id,

        title=title,
        description=description,

        source_type=source_type,

        video_url=saved_video_path,
        thumbnail_url=saved_thumbnail_path,

        open_date=open_date,
        close_date=close_date,
    )

    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return new_video


# =========================
# GET VIDEOS BY MODULE
# =========================

@router.get("/module/{module_id}", response_model=list[VideoResponse])
def get_videos(module_id: int, db: Session = Depends(get_db)):

    videos = (
        db.query(Video)
        .filter(Video.module_id == module_id)
        .all()
    )

    return videos


# =========================
# GET SINGLE VIDEO
# =========================

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):

    video = (
        db.query(Video)
        .filter(Video.id == video_id)
        .first()
    )

    if not video:
        raise HTTPException(404, "Video not found")

    return video


# =========================
# DELETE VIDEO
# =========================

@router.delete("/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):

    video = (
        db.query(Video)
        .filter(Video.id == video_id)
        .first()
    )

    if not video:
        raise HTTPException(404, "Video not found")

    # delete uploaded files
    if video.video_url and os.path.exists(video.video_url):
        try:
            os.remove(video.video_url)
        except:
            pass

    if video.thumbnail_url and os.path.exists(video.thumbnail_url):
        try:
            os.remove(video.thumbnail_url)
        except:
            pass

    db.delete(video)
    db.commit()

    return {
        "message": "Video deleted successfully"
    }