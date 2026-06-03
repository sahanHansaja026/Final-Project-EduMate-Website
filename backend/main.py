from ast import mod
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from routes import auth,profile,module,content,meeting,quiz,question,video,quiz_score,student_answer,subscription_routes,module_quota,video_quota,quiz_quota,enrollment
from chatbot import chatbot
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Serve uploads folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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

@app.get("/")
def root():
    return {"status": "API running"}
