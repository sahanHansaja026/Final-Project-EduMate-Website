from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.manual_grading import ManualGrading

router = APIRouter(prefix="/manual-grading", tags=["ManualGrading"])

@router.post("/", response_model=dict, status_code=201)
def create_manual_grading(
    assignment_id: int,
    student_id: int,
    score: float,
    feedback: str = None,
    db: Session = Depends(get_db),
):
    from app.models.manual_grading import ManualGrading
    new_grading = ManualGrading(
        assignment_id=assignment_id,
        student_id=student_id,
        score=score,
        feedback=feedback,
    )
    db.add(new_grading)
    db.commit()
    db.refresh(new_grading)
    return {"message": "Manual grading recorded", "grading_id": new_grading.grading_id}

@router.get("/student/{student_id}", response_model=list)
def get_manual_grading_by_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.manual_grading import ManualGrading
    gradings = db.query(ManualGrading).filter(ManualGrading.student_id == student_id).all()
    return [{"grading_id": g.grading_id, "assignment_id": g.assignment_id, "score": g.score, "feedback": g.feedback} for g in gradings]