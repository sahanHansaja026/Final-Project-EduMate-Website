import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from models.assignment import Assignment
from schemas.assignment import AssignmentResponse
from typing import List

router = APIRouter(prefix="/assignments", tags=["Assignments"])

UPLOAD_DIR = "uploads/assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CREATE ASSIGNMENT (Teacher)
@router.post("/", response_model=AssignmentResponse)
async def create_assignment(
    module_id: int = Form(...),
    title: str = Form(...),
    full_marks: int = Form(...),   # ✅ ADD THIS
    description: str = Form(None),
    file: UploadFile = File(None),
    open_date: date = Form(None),
    close_date: date = Form(None),
    allow_download: bool = Form(True),
    db: Session = Depends(get_db),
):
    file_path = None

    if file:
        path = f"{UPLOAD_DIR}/{file.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = path

    assignment = Assignment(
        module_id=module_id,
        title=title,
        full_marks=full_marks,   # ✅ SAVE IT
        description=description,
        file_path=file_path,
        open_date=open_date,
        close_date=close_date,
        allow_download=allow_download,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment

# GET ASSIGNMENTS BY MODULE ID
@router.get("/module/{module_id}", response_model=List[AssignmentResponse])
def get_assignments_by_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    assignments = (
        db.query(Assignment)
        .filter(Assignment.module_id == module_id)
        .all()
    )

    if not assignments:
        raise HTTPException(
            status_code=404,
            detail="No assignments found for this module"
        )

    return assignments

@router.put("/update/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    module_id: int = Form(None),
    title: str = Form(None),
    full_marks: int = Form(None),   # ✅ ADD THIS
    description: str = Form(None),
    file: UploadFile = File(None),
    open_date: date = Form(None),
    close_date: date = Form(None),
    allow_download: bool = Form(None),
    db: Session = Depends(get_db),
):
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # file update
    if file:
        path = f"{UPLOAD_DIR}/{file.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        assignment.file_path = path

    # field updates
    if module_id is not None:
        assignment.module_id = module_id

    if title is not None:
        assignment.title = title

    if full_marks is not None:   # ✅ ADD THIS
        assignment.full_marks = full_marks

    if description is not None:
        assignment.description = description

    if open_date is not None:
        assignment.open_date = open_date

    if close_date is not None:
        assignment.close_date = close_date

    if allow_download is not None:
        assignment.allow_download = allow_download

    db.commit()
    db.refresh(assignment)

    return assignment

@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # delete file if exists
    if assignment.file_path and os.path.exists(assignment.file_path):
        try:
            os.remove(assignment.file_path)
        except:
            pass

    db.delete(assignment)
    db.commit()

    return {"message": "Assignment deleted successfully"}

# get assingment using assinment id
@router.get("/{assignment_id}", response_model=AssignmentResponse)
def get_assignment_by_id(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    assignment = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return assignment