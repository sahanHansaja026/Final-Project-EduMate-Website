import os
from datetime import datetime
import traceback
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from services.s3_service import delete_file, upload_file
from database import get_db
from models.assignment_submission import AssignmentSubmission
from schemas.submission import GradeUpdate, SubmissionResponse

# Import your working S3 helper functions


router = APIRouter(prefix="/submissions", tags=["Submissions"])


# ==========================================
# STUDENT SUBMIT ASSIGNMENT
# ==========================================
@router.post("/")
async def submit_assignment(
    assignment_id: int = Form(...),
    student_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        print("\n===== SUBMISSION DEBUG START =====")
        print("assignment_id:", assignment_id)
        print("student_id:", student_id)
        print("file name:", file.filename)

        # Wrap S3 upload securely to catch credentials/network issues cleanly
        try:
            file_url = upload_file(file, folder="submissions")
            print("S3 file_url:", file_url)
        except Exception as s3_err:
            print(f"S3 UPLOAD FAILED: {str(s3_err)}")
            raise HTTPException(
                status_code=500,
                detail=f"Cloud storage upload failed. Verify AWS credentials. Dev Error: {str(s3_err)}"
            )

        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            student_id=student_id,
            file_path=file_url,
            submitted_at=datetime.utcnow(),
        )

        db.add(submission)
        db.commit()
        db.refresh(submission)

        print("DB SAVE SUCCESS")
        print("===== SUBMISSION DEBUG END =====\n")

        return submission

    except HTTPException:
        # Re-raise the clean HTTPExceptions we generated intentionally
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print("\n===== SUBMISSION ERROR =====")
        traceback.print_exc()
        print("ERROR MESSAGE:", str(e))
        print("===== END ERROR =====\n")

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

# ==========================================
# GET SUBMISSIONS BY ASSIGNMENT ID
# ==========================================
@router.get("/assignment/{assignment_id}")
def get_submissions(assignment_id: int, db: Session = Depends(get_db)):
    return (
        db.query(AssignmentSubmission)
        .filter(AssignmentSubmission.assignment_id == assignment_id)
        .all()
    )


# ==========================================
# CHECK SUBMISSION BY ASSIGNMENT & STUDENT ID
# ==========================================
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
            AssignmentSubmission.student_id == student_id,
        )
        .first()
    )

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission


# ==========================================
# DEBUG ROUTE
# ==========================================
@router.get("/assignment/{assignment_id}/student/{student_id}")
def debug_submission(
    assignment_id: int, student_id: int, db: Session = Depends(get_db)
):
    print("DEBUG assignment_id:", assignment_id)
    print("DEBUG student_id:", student_id)

    all_rows = db.query(AssignmentSubmission).all()
    print("ALL SUBMISSIONS:", all_rows)

    submission = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == student_id,
        )
        .first()
    )

    print("FOUND:", submission)

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission


# ==========================================
# UPDATE SUBMISSION GRADE
# ==========================================
@router.put("/grade/{submission_id}")
async def update_submission(
    submission_id: int,
    marks: Optional[int] = Form(None),
    file: UploadFile = File(None),   # ✅ ADD FILE UPDATE SUPPORT
    db: Session = Depends(get_db),
):
    submission = (
        db.query(AssignmentSubmission)
        .filter(AssignmentSubmission.id == submission_id)
        .first()
    )

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # =========================
    # FILE UPDATE (S3 REPLACE)
    # =========================
    if file:

        # delete old file from S3
        if submission.file_path:
            delete_file(submission.file_path)

        # upload new file
        submission.file_path = upload_file(file, "submissions")

    # =========================
    # UPDATE MARKS
    # =========================
    if marks is not None:
        submission.marks = marks

    db.commit()
    db.refresh(submission)

    return submission


# ==========================================
# DOWNLOAD / FETCH SUBMISSION FILE
# ==========================================
@router.get("/file/{submission_id}")
def get_file(submission_id: int, db: Session = Depends(get_db)):
    submission = (
        db.query(AssignmentSubmission)
        .filter(AssignmentSubmission.id == submission_id)
        .first()
    )

    if not submission or not submission.file_path:
        raise HTTPException(status_code=404, detail="Submission or file link not found")

    # ❌ OLD WAY (DO NOT DO THIS):
    # return {"file_url": submission.file_path}

    #  NEW WAY (This triggers the direct file stream download):
    return RedirectResponse(url=submission.file_path)