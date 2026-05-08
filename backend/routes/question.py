from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db

from models.question import Question
from models.question_option import QuestionOption

from schemas.question import (
    QuestionCreate,
    QuestionResponse
)

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


# CREATE QUESTION
@router.post("/", response_model=QuestionResponse)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db)
):

    new_question = Question(
        quiz_id=question_data.quiz_id,
        question_number=question_data.question_number,
        question_type=question_data.question_type,
        question_text=question_data.question_text,
        marks=question_data.marks,
        explanation=question_data.explanation,
        difficulty=question_data.difficulty,
        is_required=question_data.is_required,
        allow_negative_marking=question_data.allow_negative_marking,
        negative_marks=question_data.negative_marks,
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # add options
    if question_data.options:
        for option in question_data.options:

            new_option = QuestionOption(
                question_id=new_question.id,
                option_text=option.option_text,
                is_correct=option.is_correct
            )

            db.add(new_option)

    db.commit()
    db.refresh(new_question)

    return new_question


# GET QUESTIONS BY QUIZ
@router.get(
    "/quiz/{quiz_id}",
    response_model=List[QuestionResponse]
)
def get_questions_by_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found"
        )

    return questions


# GET SINGLE QUESTION
@router.get(
    "/{question_id}",
    response_model=QuestionResponse
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):

    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question


# DELETE QUESTION
@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):

    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    db.delete(question)

    db.commit()

    return {
        "message": "Question deleted successfully"
    }


# UPDATE QUESTION
@router.put(
    "/{question_id}",
    response_model=QuestionResponse
)
def update_question(
    question_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db)
):

    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    question.question_number = question_data.question_number
    question.question_type = question_data.question_type
    question.question_text = question_data.question_text
    question.marks = question_data.marks
    question.explanation = question_data.explanation
    question.difficulty = question_data.difficulty
    question.is_required = question_data.is_required
    question.allow_negative_marking = question_data.allow_negative_marking
    question.negative_marks = question_data.negative_marks

    # remove old options
    db.query(QuestionOption).filter(
        QuestionOption.question_id == question.id
    ).delete()

    # add new options
    if question_data.options:
        for option in question_data.options:

            new_option = QuestionOption(
                question_id=question.id,
                option_text=option.option_text,
                is_correct=option.is_correct
            )

            db.add(new_option)

    db.commit()
    db.refresh(question)

    return question
# GET ALL QUESTIONS BY QUIZ
@router.get("/quiz/{quiz_id}", response_model=List[QuestionResponse])
def get_questions_by_quiz(quiz_id: int, db: Session = Depends(get_db)):

    return db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).order_by(Question.question_number).all()
    
# GET SINGLE QUESTION
@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question

# UPDATE QUESTION (IMPROVED SAFE VERSION)
@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db)
):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # update fields
    update_data = question_data.model_dump(exclude={"options"})

    for key, value in update_data.items():
        setattr(question, key, value)

    # remove old options
    db.query(QuestionOption).filter(
        QuestionOption.question_id == question.id
    ).delete()

    # add new options
    if question_data.options:
        db.add_all([
            QuestionOption(
                question_id=question.id,
                option_text=o.option_text,
                is_correct=o.is_correct
            )
            for o in question_data.options
        ])

    db.commit()
    db.refresh(question)

    return question

# DELETE QUESTION
@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    return {"message": "Question deleted successfully"}