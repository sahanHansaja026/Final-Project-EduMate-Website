from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.subscription import Subscription
from models.channel import Channel
from models.subscription import PlanEnum

router = APIRouter(
    prefix="/quota",
    tags=["Channel Quota"]
)


@router.get("/channel/{user_id}")
def check_channel_quota(user_id: int, db: Session = Depends(get_db)):

    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == "active"
    ).first()

    # Default = free
    plan = PlanEnum.free

    if sub and sub.plan_name:
        plan = sub.plan_name

    # Count channels
    channel_count = db.query(Channel).filter(
        Channel.user_id == user_id
    ).count()

    # RULES (FIXED)
    if plan == PlanEnum.free:
        limit = 0

    elif plan in [PlanEnum.premium, PlanEnum.edu]:
        limit = 1

    else:
        limit = 0

    can_create = channel_count < limit
    remaining = max(limit - channel_count, 0)

    return {
        "user_id": user_id,
        "subscription_type": plan.value,
        "used_channels": channel_count,
        "limit": limit,
        "remaining": remaining,
        "can_create": can_create
    }