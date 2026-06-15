import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from services.s3_service import delete_file, upload_file
from database import get_db
from models.assignment import Assignment
from schemas.assignment import AssignmentResponse
from typing import List



router = APIRouter(prefix="/assignments", tags=["Assignments"])


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

    # Stream the file directly to S3 if it exists
    if file:
        try:
            file_path = upload_file(file, folder="assignments")
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload file to cloud storage: {str(e)}"
            )

    assignment = Assignment(
        module_id=module_id,
        title=title,
        full_marks=full_marks,   # ✅ SAVE IT
        description=description,
        file_path=file_path,     # Saves the S3 Object HTTPS URL string
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


# UPDATE ASSIGNMENT
@router.put("/update/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    module_id: int = Form(None),
    title: str = Form(None),
    full_marks: int = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None),
    open_date: date = Form(None),
    close_date: date = Form(None),
    allow_download: bool = Form(None),
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

    # Handle S3 file updates cleanly
    if file:
        # Delete old file from S3 if it has an active URL
        if assignment.file_path:
            delete_file(assignment.file_path)

        # Upload new replacement file to S3
        try:
            assignment.file_path = upload_file(file, folder="assignments")
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload updated file to cloud storage: {str(e)}"
            )

    # Update other model fields
    if module_id is not None:
        assignment.module_id = module_id

    if title is not None:
        assignment.title = title

    if full_marks is not None:
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


# DELETE ASSIGNMENT
@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # If the assignment contains an S3 URL asset, delete it from the bucket
    if assignment.file_path:
        delete_file(assignment.file_path)

    db.delete(assignment)
    db.commit()

    return {"message": "Assignment deleted successfully"}


# GET ASSIGNMENT BY ID
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