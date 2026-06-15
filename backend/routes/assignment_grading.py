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
    print("\n" + "="*50)
    print(f"📥 NEW REQUEST RECEIVED FOR ASSIGNMENT ID: {assignment_id}")
    print("="*50)

    # 1. Fetch assignment configuration details
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    full_marks = assignment.full_marks 

    # 2. Query the submissions table directly for this assignment
    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id
    ).all()
    
    print(f"📦 SUBMISSION CHECK: Found {len(submissions)} total submissions in database.")

    results = []

    # 3. Process the records found directly in assignment_submissions
    for sub in submissions:
        student_marks = sub.marks if sub.marks is not None else 0
        percentage = round((student_marks / full_marks) * 100, 2) if full_marks > 0 else 0

        results.append({
            "user_id": sub.student_id,  # Pulling student_id directly from submission record
            "status": "Submitted",
            "submitted_at": sub.submitted_at.isoformat() if hasattr(sub.submitted_at, 'isoformat') else str(sub.submitted_at),
            "marks": sub.marks,
            "percentage": percentage
        })

    payload_response = {
        "assignment_id": assignment_id,
        "full_marks": full_marks,
        "students": results
    }

    print("\n📤 OUTGOING PAYLOAD TO FRONTEND:")
    import json
    print(json.dumps(payload_response, indent=4, default=str))
    print("="*50 + "\n")

    return payload_response