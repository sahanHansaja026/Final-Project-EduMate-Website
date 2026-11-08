from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment_module_grade import AssignmentModuleGrade

router = APIRouter(prefix="/assignment-module-grade", tags=["AssignmentModuleGrade"])

@router.post("/", response_model=dict, status_code=201)
def create_assignment_module_grade(
    assignment_id: int,
    module_id: int,
    grade: float,
    db: Session = Depends(get_db),
):
    from app.models.assignment_module_grade import AssignmentModuleGrade
    new_grade = AssignmentModuleGrade(
        assignment_id=assignment_id,
        module_id=module_id,
        grade=grade,
    )
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return {"message": "Assignment-module grade created", "grade_id": new_grade.grade_id}

@router.get("/module/{module_id}", response_model=list)
def get_grades_by_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment_module_grade import AssignmentModuleGrade
    grades = db.query(AssignmentModuleGrade).filter(AssignmentModuleGrade.module_id == module_id).all()
    return [{"grade_id": g.grade_id, "assignment_id": g.assignment_id, "grade": g.grade} for g in grades]