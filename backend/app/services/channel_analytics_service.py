"""Business logic for channel analytics."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import authorized_student_repository, channel_repository


def get_channel_analytics(
    db: Session,
    user_id: int,
    current_user_id: int,
) -> dict:
    """Return per-channel and per-module student analytics for a channel owner.

    The endpoint requires a bearer token, so the caller is always authenticated
    and may only request analytics for their own account.
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view another user's channel analytics",
        )

    channels = channel_repository.get_channels_by_user(db, user_id)
    result = []

    for channel in channels:
        modules = channel_repository.get_modules_by_channel(
            db,
            channel.channel_id,
        )

        module_list = []
        total_students_in_channel = 0

        for module in modules:
            student_count = authorized_student_repository.count_students_by_module(
                db,
                module.module_id,
            )
            total_students_in_channel += student_count

            module_list.append({
                "module_id": module.module_id,
                "name": module.name,
                "description": module.description,
                "visibility": module.visibility,
                "cover_image": module.cover_image,
                "skills": module.skills,
                "student_count": student_count,
            })

        result.append({
            "channel_id": channel.channel_id,
            "channel_name": channel.channel_name,
            "description": channel.description,
            "visibility": channel.visibility,
            "institute_legal_name": channel.institute_legal_name,
            "modules_count": len(modules),
            "total_students": total_students_in_channel,
            "modules": module_list,
        })

    return {
        "user_id": user_id,
        "channels_count": len(result),
        "channels": result,
    }
