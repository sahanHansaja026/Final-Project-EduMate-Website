import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.assignment_submission import AssignmentSubmission
from fastapi.responses import FileResponse
from schemas.submission import GradeUpdate, SubmissionResponse

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



@router.get("/assignment/{assignment_id}/student/{student_id}")
def debug_submission(assignment_id: int, student_id: int, db: Session = Depends(get_db)):

    print("DEBUG assignment_id:", assignment_id)
    print("DEBUG student_id:", student_id)

    all_rows = db.query(AssignmentSubmission).all()
    print("ALL SUBMISSIONS:", all_rows)

    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id,
        AssignmentSubmission.student_id == student_id
    ).first()

    print("FOUND:", submission)

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission

@router.put("/grade/{submission_id}")
def update_submission_grade(
    submission_id: int,
    payload: GradeUpdate,
    db: Session = Depends(get_db),
):
    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.id == submission_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if payload.marks is not None:
        submission.marks = payload.marks

    db.commit()
    db.refresh(submission)

    return submission

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@router.get("/file/{submission_id}")
def get_file(submission_id: int, db: Session = Depends(get_db)):

    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.id == submission_id
    ).first()

    if not submission:
        raise HTTPException(404, "Not found")

    full_path = os.path.join(BASE_DIR, submission.file_path)

    if not os.path.exists(full_path):
        raise HTTPException(404, f"File missing: {full_path}")

    return FileResponse(full_path)