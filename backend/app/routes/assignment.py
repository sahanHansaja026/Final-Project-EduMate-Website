from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.assignment import Assignment

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("/", response_model=dict, status_code=201)
async def create_assignment(
    module_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    deadline: str = Form(...),
    db: Session = Depends(get_db),
):
    from app.models.module import Module
    # Validate module exists
    module = db.query(Module).filter(Module.module_id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    new_assignment = Assignment(
        module_id=module_id,
        title=title,
        description=description,
        deadline=deadline,
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return {"message": "Assignment created", "assignment_id": new_assignment.assignment_id}

@router.get("/module/{module_id}", response_model=list)
def get_assignments_by_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment import Assignment
    assignments = db.query(Assignment).filter(Assignment.module_id == module_id).all()
    return [{"assignment_id": a.assignment_id, "title": a.title, "module_id": a.module_id} for a in assignments]

@router.get("/{assignment_id}", response_model=dict)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    from app.models.assignment import Assignment
    assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {
        "assignment_id": assignment.assignment_id,
        "title": assignment.title,
        "description": assignment.description,
        "deadline": str(assignment.deadline),
    }