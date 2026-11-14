from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.authorized_student import AuthorizedStudent

router = APIRouter(prefix="/authorized-students", tags=["AuthorizedStudents"])

@router.post("/", response_model=dict, status_code=201)
def add_authorized_student(
    course_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.authorized_student import AuthorizedStudent
    new_authorized = AuthorizedStudent(
        course_id=course_id,
        student_id=student_id,
    )
    db.add(new_authorized)
    db.commit()
    db.refresh(new_authorized)
    return {"message": "Authorized student added", "authorized_id": new_authorized.authorized_id}

@router.get("/course/{course_id}", response_model=list)
def get_authorized_students(
    course_id: int,
    db: Session = Depends(get_db),
):
    from app.models.authorized_student import AuthorizedStudent
    students = db.query(AuthorizedStudent).filter(AuthorizedStudent.course_id == course_id).all()
    return [{"authorized_id": s.authorized_id, "student_id": s.student_id} for s in students]