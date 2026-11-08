from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription, PlanEnum

router = APIRouter(prefix="/module-quotas", tags=["ModuleQuotas"])

@router.get("/user/{user_id}", response_model=dict)
def get_module_quota(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        # Free plan: 1 module
        return {"remaining": 1, "used": 0, "limit": 1, "plan": "free"}
    
    plan = subscription.plan_name
    if plan == PlanEnum.free:
        limit = 1
    elif plan == PlanEnum.premium:
        limit = 10
    elif plan == PlanEnum.education:
        limit = 20
    else:
        limit = 1
    
    used = db.query(module_quota_repo).filter(...).count()  # placeholder
    
    return {
        "remaining": max(0, limit - used),
        "used": used,
        "limit": limit,
        "plan": plan.value if hasattr(plan, 'value') else str(plan),
    }