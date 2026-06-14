from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.video import Video
from models.chaneel_modules import ChannelModule
from models.authorized_student import AuthorizedStudent

router = APIRouter(
    prefix="/video-access",
    tags=["Video Access Control"]
)


@router.get("/check/{video_id}")
def check_video_access(
    video_id: int,
    user_id: int,
    student_email: str,
    db: Session = Depends(get_db)
):
    # 1. Get video
    video = db.query(Video).filter(
        Video.id == video_id
    ).first()

    if not video:
        return {"access": False}

    # 2. Get module
    module = db.query(ChannelModule).filter(
        ChannelModule.module_id == video.module_id
    ).first()

    if not module:
        return {"access": False}

    # 3. OWNER CHECK
    is_owner = module.user_id == user_id

    # 4. AUTHORIZED STUDENT CHECK
    is_student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == video.module_id,
        AuthorizedStudent.student_email == student_email,
        AuthorizedStudent.status == "active"
    ).first() is not None

    # 5. ACCESS RULE
    access = is_owner or is_student

    return {
        "video_id": video_id,
        "module_id": video.module_id,
        "access": access
    }
    
@router.get("/edit-access/{video_id}")
def check_video_edit_access(
    video_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    # 1. Get video
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        return {"access": False}

    # 2. Get module
    module = db.query(ChannelModule).filter(
        ChannelModule.module_id == video.module_id
    ).first()

    if not module:
        return {"access": False}

    # 3. ONLY OWNER CAN EDIT
    access = module.user_id == user_id

    return {
        "video_id": video_id,
        "module_id": module.module_id,
        "access": access
    }