from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.quiz_score import QuizScore

router = APIRouter(prefix="/quiz-scores", tags=["QuizScores"])

@router.post("/", response_model=dict, status_code=201)
def create_quiz_score(
    quiz_id: int,
    student_id: int,
    score: float,
    max_score: float,
    db: Session = Depends(get_db),
):
    from app.models.quiz_score import QuizScore
    new_score = QuizScore(
        quiz_id=quiz_id,
        student_id=student_id,
        score=score,
        max_score=max_score,
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return {"message": "Quiz score created", "score_id": new_score.score_id}

@router.get("/student/{student_id}", response_model=list)
def get_quiz_scores_by_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.quiz_score import QuizScore
    scores = db.query(QuizScore).filter(QuizScore.student_id == student_id).all()
    return [{"score_id": s.score_id, "quiz_id": s.quiz_id, "score": s.score, "max_score": s.max_score} for s in scores]

@router.get("/quiz/{quiz_id}", response_model=list)
def get_quiz_scores_by_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    from app.models.quiz_score import QuizScore
    scores = db.query(QuizScore).filter(QuizScore.quiz_id == quiz_id).all()
    return [{"score_id": s.score_id, "student_id": s.student_id, "score": s.score, "max_score": s.max_score} for s in scores]