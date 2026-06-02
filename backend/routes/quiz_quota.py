from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.subscription import Subscription
from models.quiz import Quiz
from models.module import Module

router = APIRouter(prefix="/quota", tags=["Quiz Quota"])


# =========================
# QUIZ QUOTA CHECK
# FREE = 3 QUIZZES TOTAL
# =========================

@router.get("/quiz/{user_id}")
def check_quiz_quota(user_id: int, db: Session = Depends(get_db)):

    # 1. Get subscription
    sub = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).first()

    plan = "free"
    if sub:
        plan = getattr(sub, "plan", None) or getattr(sub, "plan_type", None) or "free"

    is_free = plan.lower() == "free"

    # 2. Count quizzes via Module → User
    quiz_count = (
        db.query(Quiz)
        .join(Module, Quiz.module_id == Module.module_id)
        .filter(Module.user_id == user_id)
        .count()
    )

    # 3. Rules
    limit = 3 if is_free else None

    can_create = True
    if is_free:
        can_create = quiz_count < 3

    return {
        "user_id": user_id,
        "subscription_type": plan,
        "used_quizzes": quiz_count,
        "limit": limit,
        "can_create": can_create,
        "remaining": max(0, 3 - quiz_count) if is_free else "unlimited"
    }