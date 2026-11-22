"""Channel analytics endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.controllers import channel_analytics_controller
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/channel-analytics", tags=["Channel Analytics"])


@router.get("/{user_id}")
def get_channel_analytics(
    user_id: int,
    current_user_id: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return per-channel student analytics for a channel owner."""
    return channel_analytics_controller.get_channel_analytics(
        db,
        user_id=user_id,
        current_user_id=current_user_id,
        current_user=current_user,
    )
