from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from database import get_db
from models.module import Module, VisibilityEnum
from schemas.module import ModuleResponse

router = APIRouter(prefix="/modules", tags=["Modules"])

@router.post("/", response_model=ModuleResponse)
async def create_module(
    user_id: int = Form(...),  # new field
    name: str = Form(...),
    description: str = Form(None),
    skills: str = Form("[]"),  # JSON string array
    visibility: VisibilityEnum = Form(...),
    cover_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    skills_list = json.loads(skills)  # convert JSON string to list

    image_bytes = None
    image_name = None
    if cover_image:
        image_bytes = await cover_image.read()  # read file as bytes
        image_name = cover_image.filename

    new_module = Module(
        user_id=user_id,
        name=name,
        description=description,
        skills=skills_list,
        visibility=visibility,
        cover_image=image_bytes,
        cover_image_name=image_name
    )
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return ModuleResponse.from_orm(new_module)

@router.get("/user/{user_id}", response_model=List[ModuleResponse])
def get_modules_by_user(user_id: int, db: Session = Depends(get_db)):
    modules = db.query(Module).filter(Module.user_id == user_id).all()

    if not modules:
        return []

    # 🔥 CRITICAL: convert manually
    return [ModuleResponse.from_orm(m) for m in modules]


# ✅ FIRST — static route
@router.get("/public", response_model=List[ModuleResponse])
def get_public_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).filter(
        Module.visibility == "public"
    ).all()

    return [ModuleResponse.from_orm(m) for m in modules]


# ✅ THEN — dynamic route
@router.get("/{module_id}", response_model=ModuleResponse)
def get_module_by_id(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.module_id == module_id).first()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    return ModuleResponse.from_orm(module)

@router.put("/{module_id}", response_model=ModuleResponse)
async def update_module(
    module_id: int,
    user_id: int = Form(...),
    name: str = Form(None),
    description: str = Form(None),
    skills: str = Form(None),  # JSON string
    visibility: VisibilityEnum = Form(None),
    cover_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    module = db.query(Module).filter(Module.module_id == module_id).first()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # update fields only if provided
    if name is not None:
        module.name = name

    if description is not None:
        module.description = description

    if skills is not None:
        module.skills = json.loads(skills)

    if visibility is not None:
        module.visibility = visibility

    if cover_image:
        module.cover_image = await cover_image.read()
        module.cover_image_name = cover_image.filename

    db.commit()
    db.refresh(module)

    return ModuleResponse.from_orm(module)