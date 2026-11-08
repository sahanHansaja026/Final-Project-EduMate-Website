from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.quiz_attempt_controller import QuizAttemptController

router = APIRouter(prefix="/quiz-attempts", tags=["QuizAttempts"])

@router.post("/attempt", response_model=dict)
def record_quiz_attempt(
    quiz_id: int,
    user_id: int,
    score: float,
    max_score: float,
    db: Session = Depends(get_db),
):
    from app.models.quiz_attempt_controller import QuizAttemptController
    new_attempt = QuizAttemptController(
        quiz_id=quiz_id,
        user_id=user_id,
        score=score,
        max_score=max_score,
    )
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    return {"message": "Quiz attempt recorded", "attempt_id": new_attempt.attempt_id}

@router.get("/user/{user_id}/quiz/{quiz_id}", response_model=list)
def get_quiz_attempts_by_user(
    user_id: int,
    quiz_id: int,
    db: Session = Depends(get_db),
):
    from app.models.quiz_attempt_controller import QuizAttemptController
    attempts = db.query(QuizAttemptController).filter(
        QuizAttemptController.quiz_id == quiz_id,
        QuizAttemptController.user_id == user_id
    ).all()
    return [{"attempt_id": a.attempt_id, "score": a.score, "max_score": a.max_score} for a in attempts]