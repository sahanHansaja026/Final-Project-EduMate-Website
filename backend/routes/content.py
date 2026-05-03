import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from models.content import Content
from schemas.content import ContentResponse

router = APIRouter(prefix="/contents", tags=["Contents"])

UPLOAD_DIR = "uploads"

# ✅ ensure folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ CREATE CONTENT
@router.post("/", response_model=ContentResponse)
async def create_content(
    module_id: int = Form(...),
    title: str = Form(...),
    week: int = Form(...),
    description: str = Form(None),

    external_url: str = Form(None),
    file: UploadFile = File(None),

    open_date: date = Form(None),
    close_date: date = Form(None),

    allow_download: bool = Form(True),

    db: Session = Depends(get_db),
):
    file_path = None

    # ✅ Save uploaded file
    if file:
        file_location = f"{UPLOAD_DIR}/{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_path = file_location

    # ✅ If external URL
    elif external_url:
        file_path = external_url

    new_content = Content(
        module_id=module_id,
        title=title,
        week=week,
        description=description,
        file_path=file_path,
        open_date=open_date,
        close_date=close_date,
        allow_download=allow_download,
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return ContentResponse.from_orm(new_content)

@router.get("/module/{module_id}", response_model=List[ContentResponse])
def get_contents_by_module(module_id: int, db: Session = Depends(get_db)):
    contents = db.query(Content).filter(Content.module_id == module_id).all()

    if not contents:
        raise HTTPException(status_code=404, detail="No content found for this module")

    return contents