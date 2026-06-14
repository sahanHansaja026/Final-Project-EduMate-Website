from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.content import Content
from models.chaneel_modules import ChannelModule
from models.authorized_student import AuthorizedStudent

router = APIRouter(
    prefix="/content-access",
    tags=["Content Access Control"]
)


@router.get("/check/{content_id}")
def check_content_access(
    content_id: int,
    user_id: int,
    student_email: str,
    db: Session = Depends(get_db)
):
    # 1. Get content
    content = db.query(Content).filter(
        Content.assignment_id == content_id
    ).first()

    if not content:
        return {"access": False}

    # 2. Get module
    module = db.query(ChannelModule).filter(
        ChannelModule.module_id == content.module_id
    ).first()

    if not module:
        return {"access": False}

    # 3. OWNER CHECK
    is_owner = module.user_id == user_id

    # 4. STUDENT CHECK
    is_student = db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == content.module_id,
        AuthorizedStudent.student_email == student_email,
        AuthorizedStudent.status == "active"
    ).first() is not None

    # 5. FINAL RULE (OR LOGIC)
    access = is_owner or is_student

    return {
        "content_id": content_id,
        "module_id": content.module_id,
        "access": access
    }