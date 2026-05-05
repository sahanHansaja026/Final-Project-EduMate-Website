import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
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

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    title: str = Form(None),
    week: int = Form(None),
    description: str = Form(None),

    external_url: str = Form(None),
    file: UploadFile = File(None),

    open_date: date = Form(None),
    close_date: date = Form(None),

    allow_download: bool = Form(None),

    db: Session = Depends(get_db),
):
    content = db.query(Content).filter(Content.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # ✅ Handle file update
    if file:
        file_location = f"{UPLOAD_DIR}/{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        content.file_path = file_location

    elif external_url:
        content.file_path = external_url

    # ✅ Update fields only if provided
    if title is not None:
        content.title = title

    if week is not None:
        content.week = week

    if description is not None:
        content.description = description

    if open_date is not None:
        content.open_date = open_date

    if close_date is not None:
        content.close_date = close_date

    if allow_download is not None:
        content.allow_download = allow_download

    db.commit()
    db.refresh(content)

    return ContentResponse.from_orm(content)

@router.delete("/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.assignment_id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # delete file if exists
    if content.file_path and os.path.exists(content.file_path):
        try:
            os.remove(content.file_path)
        except:
            pass

    db.delete(content)
    db.commit()

    return {"message": "Content deleted successfully"}

@router.put("/update/{content_id}")
def update_content(
    content_id: int,

    title: Optional[str] = Form(None),
    week: Optional[int] = Form(None),
    description: Optional[str] = Form(None),

    external_url: Optional[str] = Form(None),

    open_date: Optional[date] = Form(None),
    close_date: Optional[date] = Form(None),

    allow_download: Optional[bool] = Form(None),

    db: Session = Depends(get_db),
):
    content = db.query(Content).filter(Content.assignment_id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # ✅ update only provided fields (PATCH-style behavior)
    if title is not None:
        content.title = title

    if week is not None:
        content.week = week

    if description is not None:
        content.description = description

    if open_date is not None:
        content.open_date = open_date

    if close_date is not None:
        content.close_date = close_date

    if allow_download is not None:
        content.allow_download = allow_download

    # (optional field — only if your model supports it)
    if external_url is not None:
        content.file_path = external_url

    db.commit()
    db.refresh(content)

    return {
        "message": "Content updated successfully",
        "data": content
    }

@router.get("/view/{content_id}")
def get_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.assignment_id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return content