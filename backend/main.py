from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from routes import auth,profile,module,content,meeting,quiz,question

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

@app.get("/")
def root():
    return {"status": "API running"}
