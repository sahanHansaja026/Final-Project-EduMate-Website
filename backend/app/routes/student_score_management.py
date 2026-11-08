from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.score_management import ScoreManagement

router = APIRouter(prefix="/student-score-management", tags=["StudentScoreManagement"])

@router.post("/", response_model=dict)
def update_student_score(
    student_id: int,
    assignment_id: int,
    score: float,
    max_score: float,
    db: Session = Depends(get_db),
):
    from app.models.score_management import ScoreManagement
    # Check if score record exists
    existing = db.query(ScoreManagement).filter(
        ScoreManagement.student_id == student_id,
        ScoreManagement.assignment_id == assignment_id
    ).first()
    
    if existing:
        existing.score = score
        existing.max_score = max_score
    else:
        new_score = ScoreManagement(
            student_id=student_id,
            assignment_id=assignment_id,
            score=score,
            max_score=max_score,
        )
        db.add(new_score)
    
    db.commit()
    return {"message": "Student score updated", "student_id": student_id, "assignment_id": assignment_id}

@router.get("/student/{student_id}", response_model=list)
def get_student_scores(
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.score_management import ScoreManagement
    scores = db.query(ScoreManagement).filter(ScoreManagement.student_id == student_id).all()
    return [{"assignment_id": s.assignment_id, "score": s.score, "max_score": s.max_score} for s in scores]