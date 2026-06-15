from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.channel import Channel
from models.chaneel_modules import ChannelModule
from models.authorized_student import AuthorizedStudent

router = APIRouter(prefix="/channel-analytics", tags=["Channel Analytics"])


@router.get("/{user_id}")
def get_channel_analytics(user_id: int, db: Session = Depends(get_db)):
    # 1. Get all channels for user
    channels = db.query(Channel).filter(Channel.user_id == user_id).all()

    result = []

    for channel in channels:
        # 2. Get modules for this channel
        modules = db.query(ChannelModule).filter(
            ChannelModule.channel_id == channel.channel_id
        ).all()

        module_list = []
        total_students_in_channel = 0

        for module in modules:
            # 3. Count students per module
            student_count = db.query(AuthorizedStudent).filter(
                AuthorizedStudent.channel_module_id == module.module_id
            ).count()

            total_students_in_channel += student_count

            module_list.append({
                "module_id": module.module_id,
                "name": module.name,
                "description": module.description,
                "visibility": module.visibility,
                "cover_image": module.cover_image,
                "skills": module.skills,
                "student_count": student_count
            })

        result.append({
            "channel_id": channel.channel_id,
            "channel_name": channel.channel_name,
            "description": channel.description,
            "visibility": channel.visibility,
            "institute_legal_name": channel.institute_legal_name,
            "modules_count": len(modules),
            "total_students": total_students_in_channel,
            "modules": module_list
        })

    return {
        "user_id": user_id,
        "channels_count": len(result),
        "channels": result
    }