from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import get_db
from models.quiz import Quiz
from models.quiz_score import QuizScore
from models.question import Question

router = APIRouter(
    prefix="/grades",
    tags=["Grades"]
)

# 1. Create a request body validation schema
class UpdateScoreRequest(BaseModel):
    obtained_marks: float = Field(..., gte=0, description="The score given by the teacher")


# Helper
def calculate_percentage(student_marks: float, max_marks: float):
    if not max_marks or max_marks <= 0:
        return 0
    return round((student_marks / max_marks) * 100, 2)


# -----------------------------
# UPDATE SCORE (TEACHER / AUTO FIXED)
# -----------------------------
@router.put("/update-score/{quiz_id}/{student_id}")
def update_scores(
    quiz_id: int,
    student_id: int,
    payload: UpdateScoreRequest,  # <-- FIX 1: Accept the body payload here
    db: Session = Depends(get_db)
):
    try:
        # ---------------- GET QUIZ SCORE ----------------
        quiz_score = db.query(QuizScore).filter(
            QuizScore.quiz_id == quiz_id,
            QuizScore.student_id == student_id
        ).first()

        if not quiz_score:
            raise HTTPException(status_code=404, detail="QuizScore not found")

        # ---------------- GET QUESTIONS ----------------
        questions = db.query(Question).filter(
            Question.quiz_id == quiz_id
        ).all()

        # ---------------- MAX MARKS ----------------
        max_marks = sum(q.marks or 0 for q in questions)

        # ---------------- STUDENT MARKS ----------------
        # FIX 2: Use the incoming value from the request body payload!
        student_marks = payload.obtained_marks  

        # ---------------- CALCULATE ----------------
        percentage = calculate_percentage(student_marks, max_marks)
        status = "pass" if percentage >= 50 else "fail"

        # ---------------- TERMINAL DEBUG ----------------
        print("\n================ QUIZ PAYLOAD ================")
        print(f"Quiz ID     : {quiz_id}")
        print(f"Student ID  : {student_id}")
        print("\n--- QUESTION MARKS ---")
        for q in questions:
            print(f"Question ID: {q.id} | Mark: {q.marks}")
        print("\n--- SUMMARY ---")
        print(f"MAX MARKS       : {max_marks}")
        print(f"STUDENT MARKS   : {student_marks}")
        print(f"PERCENTAGE      : {percentage}%")
        print(f"STATUS          : {status}")
        print("================================================\n")

        # ---------------- UPDATE DB OBJECT DIRECTLY ----------------
        # Note: Using the object directly instead of a manual .update() query
        # keeps your local object in-sync without forcing a re-fetch block.
        quiz_score.obtained_marks = student_marks # Assuming your model tracks obtained vs total
        quiz_score.total_marks = max_marks        
        quiz_score.percentage = percentage
        quiz_score.status = status

        db.commit()
        db.refresh(quiz_score)

        return {
            "message": "Grade updated successfully",
            "quiz_id": quiz_id,
            "student_id": student_id,
            "max_marks": max_marks,
            "student_marks": quiz_score.obtained_marks,
            "percentage": quiz_score.percentage,
            "status": quiz_score.status
        }

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")