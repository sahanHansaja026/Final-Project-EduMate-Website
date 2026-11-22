from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import Base, engine, init_db
from app.core.config import settings

# Create database tables using the centralized engine and declarative metadata
init_db(bind_engine=engine)

from app.routes import user, module, content, meeting, quiz, question, \
    video, quiz_score, student_answer, subscription_routes, module_quota, \
    video_quota, quiz_quota, enrollment, submission, assignment, assignemnt_quota, \
    channel, channel_quota, channel_modules, usercomments, grade, manual_grading, \
    sentiment, assignment_grading, enrollment_analytics, authorized_students, \
    channel_module_access_controller, module_quiz_access_controller, quiz_attempt_controller, \
    assignment_edit_access, channel_content_access_controller, video_access_control, \
    assignment_view_access, student_enrolle_count_channal, student_score_management, \
    channel_analytic, assignment_grade_access, assignement_module_grade, module_routes, \
    subscription_payment, chatbot

app = FastAPI()


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Map database failures to a generic server error response.

    Internal driver details (connection strings, credentials, etc.) are never
    exposed to the client.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred. Please try again later."},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(module.router)
app.include_router(content.router)
app.include_router(meeting.router)
app.include_router(quiz.router)
app.include_router(question.router)
app.include_router(video.router)
app.include_router(chatbot.router)
app.include_router(quiz_score.router)
app.include_router(student_answer.router)
app.include_router(subscription_routes.router)
app.include_router(module_quota.router)
app.include_router(video_quota.router)
app.include_router(quiz_quota.router)
app.include_router(enrollment.router)
app.include_router(submission.router)
app.include_router(assignment.router)
app.include_router(assignemnt_quota.router)
app.include_router(channel.router)
app.include_router(channel_quota.router)
app.include_router(channel_modules.router)
app.include_router(usercomments.router)
app.include_router(grade.router)
app.include_router(manual_grading.router)
app.include_router(sentiment.router)
app.include_router(assignment_grading.router)
app.include_router(enrollment_analytics.router)
app.include_router(authorized_students.router)
app.include_router(channel_module_access_controller.router)
app.include_router(module_quiz_access_controller.router)
app.include_router(quiz_attempt_controller.router)
app.include_router(assignment_edit_access.router)
app.include_router(channel_content_access_controller.router)
app.include_router(video_access_control.router)
app.include_router(assignment_view_access.router)
app.include_router(student_enrolle_count_channal.router)
app.include_router(student_score_management.router)
app.include_router(channel_analytic.router)
app.include_router(assignment_grade_access.router)
app.include_router(assignement_module_grade.router)
app.include_router(module_routes.router)
app.include_router(subscription_payment.router)


@app.get("/")
def root():
    return {"status": "API running"}