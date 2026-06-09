from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from database import get_db

from models.question import Question
from models.student_answer import StudentAnswer
from models.quiz_score import QuizScore

router = APIRouter(
    prefix="/manual-grading",
    tags=["Manual Grading"]
)

# =========================
# RESPONSE SCHEMA
# =========================

class ManualGradeItem(BaseModel):
    question_id: int
    question_text: str
    question_marks: float
    student_answer: Optional[str]
    obtained_score: float

    class Config:
        from_attributes = True


class ManualGradeUpdate(BaseModel):
    quiz_id: int
    student_id: int
    question_id: int
    score: float


# =========================
# GET GRADING VIEW
# =========================

@router.get(
    "/quiz/{quiz_id}/student/{student_id}",
    response_model=List[ManualGradeItem]
)
def get_manual_grading_view(
    quiz_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .order_by(Question.question_number)
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found"
        )

    result = []

    for q in questions:

        answer = (
            db.query(StudentAnswer)
            .filter(
                StudentAnswer.quiz_id == quiz_id,
                StudentAnswer.student_id == student_id,
                StudentAnswer.question_id == q.id
            )
            .first()
        )

        result.append({
            "question_id": q.id,
            "question_text": q.question_text,
            "question_marks": q.marks,
            "student_answer": answer.answer_text if answer else None,
            "obtained_score": answer.obtained_marks if answer else 0
        })

    return result


# =========================
# UPDATE SCORE + PERCENTAGE
# =========================

@router.put("/update-score")
def update_manual_score(
    data: ManualGradeUpdate,
    db: Session = Depends(get_db)
):

    # Find answer
    answer = db.query(StudentAnswer).filter(
        StudentAnswer.quiz_id == data.quiz_id,
        StudentAnswer.student_id == data.student_id,
        StudentAnswer.question_id == data.question_id
    ).first()

    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Answer not found"
        )

    # Update score for this answer
    answer.obtained_marks = data.score

    db.commit()

    # -----------------------------
    # Calculate obtained marks
    # -----------------------------
    answers = db.query(StudentAnswer).filter(
        StudentAnswer.quiz_id == data.quiz_id,
        StudentAnswer.student_id == data.student_id
    ).all()

    obtained_marks = sum(
        a.obtained_marks or 0
        for a in answers
    )

    # -----------------------------
    # Calculate total quiz marks
    # -----------------------------
    questions = db.query(Question).filter(
        Question.quiz_id == data.quiz_id
    ).all()

    total_marks = sum(
        q.marks or 0
        for q in questions
    )

    # -----------------------------
    # Calculate percentage
    # -----------------------------
    percentage = 0

    if total_marks > 0:
        percentage = round(
            (obtained_marks / total_marks) * 100,
            2
        )

    # -----------------------------
    # Update QuizScore table
    # -----------------------------
    quiz_score = db.query(QuizScore).filter(
        QuizScore.quiz_id == data.quiz_id,
        QuizScore.student_id == data.student_id
    ).first()

    if quiz_score:

        quiz_score.obtained_marks = obtained_marks
        quiz_score.total_marks = total_marks
        quiz_score.percentage = percentage

    else:

        quiz_score = QuizScore(
            quiz_id=data.quiz_id,
            student_id=data.student_id,
            obtained_marks=obtained_marks,
            total_marks=total_marks,
            percentage=percentage
        )

        db.add(quiz_score)

    db.commit()
    db.refresh(quiz_score)

    return {
        "message": "Score updated successfully",
        "quiz_id": data.quiz_id,
        "student_id": data.student_id,
        "obtained_marks": obtained_marks,
        "total_marks": total_marks,
        "percentage": percentage
    }