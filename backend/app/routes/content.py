from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.content import Content
from app.schemas.content import ContentResponse

router = APIRouter(prefix="/content", tags=["Content"])

@router.post("/", response_model=ContentResponse, status_code=201)
def create_content(
    title: str = Form(...),
    module_id: int = Form(...),
    url: str = Form(...),
    type: str = Form(...),
    db: Session = Depends(get_db),
):
    # Check if module exists
    from app.models.module import Module
    module = db.query(Module).filter(Module.module_id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    new_content = Content(
        title=title,
        module_id=module_id,
        url=url,
        type=type,
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return ContentResponse.from_orm(new_content)

@router.get("/{content_id}", response_model=ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse.from_orm(content)

@router.get("/module/{module_id}", response_model=list[ContentResponse])
def get_content_by_module(module_id: int, db: Session = Depends(get_db)):
    contents = db.query(Content).filter(Content.module_id == module_id).all()
    return [ContentResponse.from_orm(c) for c in contents]