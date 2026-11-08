from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.module import Module

router = APIRouter(prefix="/module-routes", tags=["ModuleRoutes"])

@router.get("/search", response_model=list)
def search_modules(
    query: str,
    db: Session = Depends(get_db),
):
    from app.models.module import Module, VisibilityEnum
    modules = db.query(Module).filter(
        Module.name.contains(query) | Module.description.contains(query)
    ).all()
    return [{"module_id": m.module_id, "name": m.name, "description": m.description} for m in modules]

@router.get("/filter", response_model=list)
def filter_modules(
    visibility: str = None,
    db: Session = Depends(get_db),
):
    from app.models.module import Module
    modules_query = db.query(Module)
    if visibility:
        modules_query = modules_query.filter(Module.visibility == visibility)
    modules = modules_query.all()
    return [{"module_id": m.module_id, "name": m.name, "visibility": m.visibility} for m in modules]