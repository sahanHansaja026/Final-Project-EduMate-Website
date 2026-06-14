from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.subscription import Subscription
from models.module import Module
from models.video import Video

router = APIRouter(prefix="/quota", tags=["Video Quota"])


@router.get("/video/{user_id}")
def check_video_quota(user_id: int, db: Session = Depends(get_db)):

    # 1. Get subscription
    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == "active"
    ).first()

    # default = free
    plan = "free"

    if sub:
        plan = sub.plan_name.value  # IMPORTANT FIX

    is_free = plan == "free"

    # 2. Count videos created by this user via Module relation
    video_count = (
        db.query(Video)
        .join(Module, Video.module_id == Module.module_id)
        .filter(Module.user_id == user_id)
        .count()
    )

    # 3. Quota rules
    if is_free:
        limit = 1
        can_create = video_count < limit
        remaining = max(0, limit - video_count)
    else:
        limit = None
        can_create = True
        remaining = "unlimited"

    return {
        "user_id": user_id,
        "subscription_type": plan,
        "used_videos": video_count,
        "limit": limit,
        "can_create": can_create,
        "remaining": remaining
    }