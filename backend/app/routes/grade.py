from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.grade import Grade

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.post("/", response_model=dict, status_code=201)
def create_grade(
    assignment_id: int,
    student_id: int,
    score: float,
    max_score: float,
    db: Session = Depends(get_db),
):
    from app.models.grade import Grade
    new_grade = Grade(
        assignment_id=assignment_id,
        student_id=student_id,
        score=score,
        max_score=max_score,
    )
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return {"message": "Grade created", "grade_id": new_grade.grade_id}

@router.get("/student/{student_id}", response_model=list)
def get_grades_by_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.grade import Grade
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    return [{"grade_id": g.grade_id, "assignment_id": g.assignment_id, "score": g.score, "max_score": g.max_score} for g in grades]

@router.get("/assignment/{assignment_id}", response_model=list)
def get_grades_by_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    from app.models.grade import Grade
    grades = db.query(Grade).filter(Grade.assignment_id == assignment_id).all()
    return [{"grade_id": g.grade_id, "student_id": g.student_id, "score": g.score, "max_score": g.max_score} for g in grades]