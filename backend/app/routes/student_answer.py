from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.student_answer import StudentAnswer

router = APIRouter(prefix="/student-answers", tags=["StudentAnswers"])

@router.post("/", response_model=dict, status_code=201)
def create_student_answer(
    quiz_id: int,
    student_id: int,
    question_id: int,
    selected_option: int,
    is_correct: bool,
    db: Session = Depends(get_db),
):
    from app.models.student_answer import StudentAnswer
    new_answer = StudentAnswer(
        quiz_id=quiz_id,
        student_id=student_id,
        question_id=question_id,
        selected_option=selected_option,
        is_correct=is_correct,
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return {"message": "Student answer recorded", "answer_id": new_answer.answer_id}

@router.get("/student/{student_id}", response_model=list)
def get_student_answers(
    student_id: int,
    db: Session = Depends(get_db),
):
    from app.models.student_answer import StudentAnswer
    answers = db.query(StudentAnswer).filter(StudentAnswer.student_id == student_id).all()
    return [{"answer_id": a.answer_id, "question_id": a.question_id, "selected_option": a.selected_option, "is_correct": a.is_correct} for a in answers]