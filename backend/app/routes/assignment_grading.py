from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment_grading import AssignmentGrading

router = APIRouter(prefix="/assignment-grading", tags=["AssignmentGrading"])

@router.post("/", response_model=dict, status_code=201)
def create_assignment_grading(
    assignment_id: int,
    student_id: int,
    score: float,
    max_score: float,
    db: Session = Depends(get_db),
):
    from app.models.assignment_grading import AssignmentGrading
    new_grading = AssignmentGrading(
        assignment_id=assignment_id,
        student_id=student_id,
        score=score,
        max_score=max_score,
    )
    db.add(new_grading)
    db.commit()
    db.refresh(new_grading)
    return {"message": "Assignment grading recorded", "grading_id": new_grading.grading_id}

@router.get("/student/{student_id}", response_model=list)
def get_assignment_grading_by_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_grading import AssignmentGrading
    gradings = db.query(AssignmentGrading).filter(AssignmentGrading.student_id == student_id).all()
    return [{"grading_id": g.grading_id, "assignment_id": g.assignment_id, "score": g.score, "max_score": g.max_score} for g in gradings]