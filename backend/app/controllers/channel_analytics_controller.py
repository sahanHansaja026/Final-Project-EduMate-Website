"""HTTP handling layer for channel analytics."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.services import channel_analytics_service


def get_channel_analytics(
    db: Session,
    user_id: int,
    current_user_id: Optional[int] = None,
    current_user: Optional[User] = None,
) -> dict:
    """Return channel analytics for a channel owner."""
    actor_user_id = current_user_id

    if current_user is not None:
        if current_user_id is not None and current_user.user_id != current_user_id:
            raise HTTPException(
                status_code=403,
                detail="Authenticated user does not match current_user_id",
            )
        actor_user_id = current_user.user_id

    return channel_analytics_service.get_channel_analytics(
        db,
        user_id=user_id,
        current_user_id=actor_user_id,
    )
