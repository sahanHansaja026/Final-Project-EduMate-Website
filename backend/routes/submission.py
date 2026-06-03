import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.assignment_submission import AssignmentSubmission
from schemas.submission import SubmissionResponse

router = APIRouter(prefix="/submissions", tags=["Submissions"])

UPLOAD_DIR = "uploads/submissions"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# STUDENT SUBMIT ASSIGNMENT
@router.post("/", response_model=SubmissionResponse)
async def submit_assignment(
    assignment_id: int = Form(...),
    student_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    submission = AssignmentSubmission(
        assignment_id=assignment_id,
        student_id=student_id,
        file_path=file_path,
        submitted_at=datetime.utcnow(),
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission

# get submition using assingment_id
@router.get("/assignment/{assignment_id}")
def get_submissions(assignment_id: int, db: Session = Depends(get_db)):
    return db.query(AssignmentSubmission)\
        .filter(AssignmentSubmission.assignment_id == assignment_id)\
        .all()
# get details using assingment_id and user id
@router.get("/check/{assignment_id}/{student_id}")
def get_submission_by_user(
    assignment_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    submission = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == student_id
        )
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )

    return submission