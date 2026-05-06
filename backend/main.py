from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

from routes import auth,profile,module,content,meeting,quiz

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

@app.get("/")
def root():
    return {"status": "API running"}
