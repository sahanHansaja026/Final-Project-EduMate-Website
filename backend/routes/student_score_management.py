from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from models.quiz import Quiz
from models.quiz_score import QuizScore
from models.assignment import Assignment
from models.assignment_submission import AssignmentSubmission

router = APIRouter(prefix="/student-score", tags=["Student Score Management"])


@router.get("/{student_id}/{module_id}")
def student_score_management(
    student_id: int,
    module_id: int,
    db: Session = Depends(get_db)
):
    """
    Get student performance for a specific module
    (quizzes + assignments + scores)
    """

    # =========================
    # QUIZZES IN MODULE
    # =========================
    quizzes = db.query(Quiz).filter(
        Quiz.module_id == module_id
    ).all()

    quiz_ids = [q.id for q in quizzes]

    quiz_scores = db.query(QuizScore).filter(
        QuizScore.student_id == student_id,
        QuizScore.quiz_id.in_(quiz_ids) if quiz_ids else False
    ).all()

    quiz_data = []

    total_quiz_marks = 0
    total_quiz_obtained = 0

    for qs in quiz_scores:
        quiz = next((q for q in quizzes if q.id == qs.quiz_id), None)

        total_quiz_marks += qs.total_marks or 0
        total_quiz_obtained += qs.obtained_marks or 0

        quiz_data.append({
            "quiz_id": qs.quiz_id,
            "title": quiz.title if quiz else None,
            "attempt_number": qs.attempt_number,
            "total_marks": qs.total_marks,
            "obtained_marks": qs.obtained_marks,
            "percentage": qs.percentage,
            "correct_answers": qs.correct_answers,
            "wrong_answers": qs.wrong_answers,
            "skipped_answers": qs.skipped_answers,
            "status": qs.status,
            "submitted_at": qs.submitted_at
        })

    # =========================
    # ASSIGNMENTS IN MODULE
    # =========================
    assignments = db.query(Assignment).filter(
        Assignment.module_id == module_id
    ).all()

    assignment_ids = [a.id for a in assignments]

    submissions = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.student_id == student_id,
        AssignmentSubmission.assignment_id.in_(assignment_ids) if assignment_ids else False
    ).all()

    assignment_data = []

    total_assignment_marks = 0
    total_assignment_obtained = 0

    for sub in submissions:
        assignment = next(
            (a for a in assignments if a.id == sub.assignment_id),
            None
        )

        full_marks = assignment.full_marks if assignment else 0

        total_assignment_marks += full_marks
        total_assignment_obtained += sub.marks or 0

        assignment_data.append({
            "assignment_id": sub.assignment_id,
            "title": assignment.title if assignment else None,
            "submitted_at": sub.submitted_at,
            "marks": sub.marks,
            "full_marks": full_marks,
            "feedback": sub.feedback,
            "file_path": sub.file_path
        })

    # =========================
    # FINAL SUMMARY
    # =========================
    total_marks = total_quiz_marks + total_assignment_marks
    total_obtained = total_quiz_obtained + total_assignment_obtained

    overall_percentage = (
        (total_obtained / total_marks * 100)
        if total_marks > 0 else 0
    )

    return {
        "student_id": student_id,
        "module_id": module_id,

        "summary": {
            "quiz_total_marks": total_quiz_marks,
            "quiz_obtained_marks": total_quiz_obtained,

            "assignment_total_marks": total_assignment_marks,
            "assignment_obtained_marks": total_assignment_obtained,

            "total_marks": total_marks,
            "total_obtained": total_obtained,
            "overall_percentage": round(overall_percentage, 2)
        },

        "quizzes": quiz_data,
        "assignments": assignment_data
    }