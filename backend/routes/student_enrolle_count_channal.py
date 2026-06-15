from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict
from models.channel import Channel   # your channel model
from models.profile import Profile
from database import get_db
from models.authorized_student import AuthorizedStudent
from models.chaneel_modules import ChannelModule
from models.enrollment import Enrollment

router = APIRouter(
    prefix="/student-channel-count",
    tags=["Student Channel Count"]
)


@router.get("/{student_email}")
def get_student_channel_count(
    student_email: str,
    db: Session = Depends(get_db)
):
    # Get all module enrollments of student
    enrollments = (
        db.query(AuthorizedStudent)
        .filter(
            AuthorizedStudent.student_email == student_email
        )
        .all()
    )

    if not enrollments:
        return {
            "student_email": student_email,
            "channel_count": 0,
            "channel_ids": []
        }

    module_ids = [e.channel_module_id for e in enrollments]

    # Get modules
    modules = (
        db.query(ChannelModule)
        .filter(
            ChannelModule.module_id.in_(module_ids)
        )
        .all()
    )

    # Unique channel ids
    unique_channel_ids = list(
        set(module.channel_id for module in modules)
    )

    return {
        "student_email": student_email,
        "channel_count": len(unique_channel_ids),
        "channel_ids": unique_channel_ids
    }
    



@router.get("/enrolled-channels/{student_email}")
def get_student_enrolled_channels(
    student_email: str,
    db: Session = Depends(get_db)
):
    # Get all student enrollments
    enrollments = (
        db.query(AuthorizedStudent)
        .filter(
            AuthorizedStudent.student_email == student_email
        )
        .all()
    )

    if not enrollments:
        return []

    # Get module ids
    module_ids = [e.channel_module_id for e in enrollments]

    # Get modules
    modules = (
        db.query(ChannelModule)
        .filter(
            ChannelModule.module_id.in_(module_ids)
        )
        .all()
    )

    grouped_channels = defaultdict(list)

    for module in modules:

        # Get instructor profile
        instructor = (
            db.query(Profile)
            .filter(Profile.id == module.user_id)
            .first()
        )

        instructor_name = None

        if instructor:
            instructor_name = (
                f"{instructor.first_name} {instructor.last_name}"
            ).strip()

        grouped_channels[module.channel_id].append({
            "moduleId": module.module_id,
            "moduleName": module.name,
            "instructor": instructor_name,
            "userId": module.user_id
        })

    result = []

    for channel_id, modules_list in grouped_channels.items():

        # Get channel
        channel = (
            db.query(Channel)
            .filter(
                Channel.channel_id == channel_id
            )
            .first()
        )

        result.append({
            "channelId": channel_id,
            "channelName": channel.channel_name if channel else None,
            "modules": modules_list
        })

    return result

@router.get("/enrollement_count/")
def get_total_enrolled_module_count(
    email: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    # -------------------------
    # 1. Channel Modules (by email)
    # -------------------------
    channel_module_ids = {
        row.channel_module_id
        for row in db.query(AuthorizedStudent)
        .filter(AuthorizedStudent.student_email == email)
        .all()
    }

    # -------------------------
    # 2. Normal Modules (by user_id)
    # -------------------------
    enrollment_module_ids = {
        row.module_id
        for row in db.query(Enrollment)
        .filter(Enrollment.user_id == user_id)
        .all()
    }

    # -------------------------
    # 3. Combine unique modules
    # -------------------------
    unique_modules = channel_module_ids.union(enrollment_module_ids)

    return {
        "email": email,
        "user_id": user_id,
        "channel_modules": len(channel_module_ids),
        "normal_modules": len(enrollment_module_ids),
        "total_modules": len(unique_modules)
    }