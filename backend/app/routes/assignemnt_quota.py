from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription, PlanEnum

router = APIRouter(prefix="/assignment-quotas", tags=["AssignmentQuotas"])

@router.get("/user/{user_id}", response_model=dict)
def get_assignment_quota(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        # Free plan: 5 assignments
        return {"remaining": 5, "used": 0, "limit": 5, "plan": "free"}
    
    plan = subscription.plan_name
    if plan == PlanEnum.free:
        limit = 5
    elif plan == PlanEnum.premium:
        limit = 200
    elif plan == PlanEnum.education:
        limit = 500
    else:
        limit = 5
    
    return {
        "remaining": max(0, limit - 0),  # placeholder for actual usage
        "used": 0,  # placeholder
        "limit": limit,
        "plan": plan.value if hasattr(plan, 'value') else str(plan),
    }