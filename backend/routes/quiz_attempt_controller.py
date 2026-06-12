from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.quiz import Quiz
from models.quiz_score import QuizScore

router = APIRouter(
    prefix="/quiz-attempts",
    tags=["Quiz Attempts"]
)


@router.get("/check/{quiz_id}/student/{student_id}")
def check_quiz_attempt_access(
    quiz_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):

    # 1. Get quiz
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 2. Use real quiz id
    real_quiz_id = quiz.id
    

    # 3. Count attempts
    attempt_count = db.query(QuizScore).filter(
        QuizScore.quiz_id == real_quiz_id,
        QuizScore.student_id == int(student_id)
    ).count()

    # 🔥 DEBUG PRINT (MUST BE HERE)
    print("FINAL ATTEMPT RESPONSE:", {
        "quiz_id": quiz_id,
        "student_id": student_id,
        "count": attempt_count
    })

    # 4. Unlimited case
    if quiz.attempts == "unlimited":
        return {
            "can_attempt": True,
            "attempts_used": attempt_count,
            "remaining_attempts": "unlimited",
            "limit": "unlimited",
        }

    # 5. Convert safely
    max_attempts = int(quiz.attempts)

    return {
        "can_attempt": attempt_count < max_attempts,
        "attempts_used": attempt_count,
        "remaining_attempts": max(max_attempts - attempt_count, 0),
        "limit": max_attempts,
    }