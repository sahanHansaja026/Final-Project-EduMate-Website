from ast import mod
from multiprocessing import AuthenticationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from fastapi.staticfiles import StaticFiles
from routes import auth,profile,module,content,meeting,quiz,question,video,quiz_score,student_answer,subscription_routes,module_quota,video_quota,quiz_quota,enrollment,submission,assignment,assignemnt_quota,channel,channel_quota,channel_modules,usercomments, grade, manual_grading,sentiment,assignment_grading,enrollment_analytics,authorized_students,channel_module_access_controller,module_quiz_access_controller,quiz_attempt_controller,assignment_edit_access
from chatbot import chatbot
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
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

@app.get("/")
def root():
    return {"status": "API running"}
