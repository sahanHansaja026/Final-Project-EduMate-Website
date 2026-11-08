from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription, PlanEnum

router = APIRouter(prefix="/channel-quotas", tags=["ChannelQuotas"])

@router.get("/user/{user_id}", response_model=dict)
def get_channel_quota(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        # Free plan: 1 channel
        return {"remaining": 1, "used": 0, "limit": 1, "plan": "free"}
    
    plan = subscription.plan_name
    if plan == PlanEnum.free:
        limit = 1
    elif plan == PlanEnum.premium:
        limit = 10
    elif plan == PlanEnum.education:
        limit = 50
    else:
        limit = 1
    
    return {
        "remaining": max(0, limit - 0),  # placeholder for actual usage
        "used": 0,  # placeholder
        "limit": limit,
        "plan": plan.value if hasattr(plan, 'value') else str(plan),
    }