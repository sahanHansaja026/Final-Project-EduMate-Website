from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.authorized_student import AuthorizedStudent
from schemas.authorized_student import (
    AuthorizedStudentCreate,
    AuthorizedStudentUpdate,
    AuthorizedStudentResponse
)

router = APIRouter(
    prefix="/authorized-students",
    tags=["Authorized Students"]
)

# add students
@router.post("/", response_model=AuthorizedStudentResponse)
def add_student(
    payload: AuthorizedStudentCreate,
    db: Session = Depends(get_db)
):

    student = AuthorizedStudent(**payload.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return student
# get studnet by module id
@router.get("/module/{module_id}")
def get_students_by_module(
    module_id: int,
    db: Session = Depends(get_db)
):
    return db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == module_id
    ).all()
    
# delete student
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student removed successfully"
    }
    
@router.put("/{student_id}", response_model=AuthorizedStudentResponse)
def update_student(
    student_id: int,
    payload: AuthorizedStudentUpdate,
    db: Session = Depends(get_db)
):

    student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # update only provided fields
    if payload.status is not None:
        student.status = payload.status

    if payload.remark is not None:
        student.remark = payload.remark

    db.commit()
    db.refresh(student)

    return student

@router.get("/{student_id}")
def get_student_by_id(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": student.id,
        "channel_module_id": student.channel_module_id,
        "student_name": student.student_name,
        "student_email": student.student_email,
        "admission_date": student.admission_date,
        "status": student.status,
        "remark": student.remark,
    }