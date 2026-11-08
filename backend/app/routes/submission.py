from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment_submission import AssignmentSubmission
from app.models.module import Module

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.post("/", response_model=dict, status_code=201)
async def create_submission(
    module_id: int = Form(...),
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate module exists
    module = db.query(Module).filter(Module.module_id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    file_bytes = await file.read()
    new_submission = AssignmentSubmission(
        assignment_id=module_id,  # Using module_id as assignment_id placeholder
        student_id=user_id,
        file_path=file_bytes.hex(),  # Store file as hex for simplicity
        filename=file.filename,
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Submission created", "submission_id": new_submission.id}

@router.get("/user/{user_id}", response_model=list)
def get_submissions_by_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    submissions = db.query(AssignmentSubmission).filter(AssignmentSubmission.student_id == user_id).all()
    return [{"submission_id": s.id, "file_path": s.file_path, "filename": s.filename} for s in submissions]

@router.get("/module/{module_id}", response_model=list)
def get_submissions_by_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    submissions = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == module_id).all()
    return [{"submission_id": s.id, "student_id": s.student_id, "filename": s.filename} for s in submissions]