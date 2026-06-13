import os
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from services.s3_service import delete_file, upload_file
from database import get_db
from models.video import Video
from schemas.video import VideoResponse

# Import your working S3 helper functions


router = APIRouter(prefix="/videos", tags=["Videos"])


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
    # SAVE VIDEO FILE (S3 OR URL)
    # =========================
    if source_type == "Upload":
        if not video_file:
            raise HTTPException(
                status_code=400,
                detail="Video file is required when source type is 'Upload'",
            )
        try:
            # Stream directly to the S3 bucket under the "videos" folder
            saved_video_path = upload_file(video_file, folder="videos")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload video to S3 cloud storage: {str(e)}",
            )
    else:
        # Fall back to incoming external text link (e.g., YouTube, Vimeo)
        saved_video_path = video_url

    # =========================
    # SAVE THUMBNAIL TO S3
    # =========================
    if thumbnail:
        try:
            # Stream directly to the S3 bucket under the "thumbnails" folder
            saved_thumbnail_path = upload_file(thumbnail, folder="thumbnails")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload thumbnail to S3 cloud storage: {str(e)}",
            )

    # =========================
    # SAVE DB RECORD
    # =========================
    new_video = Video(
        module_id=module_id,
        title=title,
        description=description,
        source_type=source_type,
        video_url=saved_video_path,  # Stores final S3 video URL or raw text link
        thumbnail_url=saved_thumbnail_path,  # Stores final S3 thumbnail URL
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
    videos = db.query(Video).filter(Video.module_id == module_id).all()
    return videos


# =========================
# GET SINGLE VIDEO
# =========================
@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(404, "Video not found")

    return video


# =========================
# DELETE VIDEO
# =========================
@router.delete("/{video_id}")
def delete_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # 1. Clear out upload-based files from your S3 bucket
    if video.source_type == "Upload" and video.video_url:
        delete_file(video.video_url)

    # 2. Clear out thumbnails from your S3 bucket
    if video.thumbnail_url:
        delete_file(video.thumbnail_url)

    db.delete(video)
    db.commit()

    return {"message": "Video deleted successfully"}


# =========================
# UPDATE VIDEO (PUT)
# =========================
@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(
    video_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    source_type: str = Form(...),
    video_url: Optional[str] = Form(None),
    video_file: Optional[UploadFile] = File(None),
    thumbnail: Optional[UploadFile] = File(None),
    open_date: Optional[date] = Form(None),
    close_date: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(
            status_code=404, detail="Video resource not found"
        )

    # Handle conditional video source alterations
    if source_type == "Upload":
        if video_file:
            # Drop previous S3 video resource if it exists
            if video.source_type == "Upload" and video.video_url:
                delete_file(video.video_url)

            # Upload new asset stream straight into S3
            try:
                video.video_url = upload_file(video_file, folder="videos")
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload new video file to S3: {str(e)}",
                )
    else:
        # If toggling from 'Upload' -> an external web link, clear old S3 asset first
        if video.source_type == "Upload" and video.video_url:
            delete_file(video.video_url)

        video.video_url = video_url

    # Handle structural thumbnail swaps
    if thumbnail:
        # Drop previous S3 thumbnail out of the bucket
        if video.thumbnail_url:
            delete_file(video.thumbnail_url)

        # Upload new graphic resource directly to S3
        try:
            video.thumbnail_url = upload_file(thumbnail, folder="thumbnails")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload new thumbnail file to S3: {str(e)}",
            )

    # Commit metadata fields down to database
    video.title = title
    video.description = description
    video.source_type = source_type
    video.open_date = open_date
    video.close_date = close_date

    db.commit()
    db.refresh(video)

    return video