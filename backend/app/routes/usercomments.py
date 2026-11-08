from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user_comments import UserComment

router = APIRouter(prefix="/user-comments", tags=["UserComments"])

@router.post("/", response_model=dict, status_code=201)
def create_user_comment(
    module_id: int,
    user_id: int,
    rating: int,
    comment_text: str,
    db: Session = Depends(get_db),
):
    from app.models.user_comments import UserComment
    new_comment = UserComment(
        module_id=module_id,
        user_id=user_id,
        rating=rating,
        comment=comment_text,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": "Comment created", "comment_id": new_comment.comment_id}

@router.get("/module/{module_id}", response_model=list)
def get_comments_by_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    from app.models.user_comments import UserComment
    comments = db.query(UserComment).filter(UserComment.module_id == module_id).all()
    return [{"comment_id": c.comment_id, "user_id": c.user_id, "rating": c.rating, "comment": c.comment} for c in comments]