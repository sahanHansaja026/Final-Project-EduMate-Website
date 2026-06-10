from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.enrollment import Enrollment
from models.assignment_submission import AssignmentSubmission
from models.assignment import Assignment

router = APIRouter(
    prefix="/assignment_grading",
    tags=["Assignment Grading"]
)


@router.get("/{assignment_id}")
def get_assignment_grading(
    assignment_id: int,
    db: Session = Depends(get_db)
):

    # check assignment exists
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    module_id = assignment.module_id
    full_marks = assignment.full_marks  # ✅ FIX: use real max marks

    # enrolled students
    enrollments = db.query(Enrollment).filter(
        Enrollment.module_id == module_id
    ).all()

    results = []

    for enrollment in enrollments:

        submission = db.query(AssignmentSubmission).filter(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == enrollment.user_id
        ).first()

        if submission and submission.marks is not None and full_marks > 0:

            percentage = round((submission.marks / full_marks) * 100, 2)

            results.append({
                "user_id": enrollment.user_id,
                "status": "Submitted",
                "submitted_at": submission.submitted_at,
                "marks": submission.marks,
                "percentage": percentage
            })

        elif submission:

            results.append({
                "user_id": enrollment.user_id,
                "status": "Submitted",
                "submitted_at": submission.submitted_at,
                "marks": submission.marks,
                "percentage": 0
            })

        else:
            results.append({
                "user_id": enrollment.user_id,
                "status": "Not Submitted",
                "submitted_at": None,
                "marks": None,
                "percentage": 0
            })

    return {
        "assignment_id": assignment_id,
        "full_marks": full_marks,   # ✅ FIX: better naming
        "students": results
    }