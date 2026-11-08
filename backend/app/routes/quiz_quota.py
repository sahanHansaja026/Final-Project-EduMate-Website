from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription, PlanEnum

router = APIRouter(prefix="/quiz-quotas", tags=["QuizQuotas"])

@router.get("/user/{user_id}", response_model=dict)
def get_quiz_quota(
    user_id: int,
    db: Session = Depends(get_db),
):
    from app.models.subscription import Subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        # Free plan: 3 quizzes
        return {"remaining": 3, "used": 0, "limit": 3, "plan": "free"}
    
    plan = subscription.plan_name
    if plan == PlanEnum.free:
        limit = 3
    elif plan == PlanEnum.premium:
        limit = 100
    elif plan == PlanEnum.education:
        limit = 200
    else:
        limit = 3
    
    return {
        "remaining": max(0, limit - 0),  # placeholder for actual usage
        "used": 0,  # placeholder
        "limit": limit,
        "plan": plan.value if hasattr(plan, 'value') else str(plan),
    }