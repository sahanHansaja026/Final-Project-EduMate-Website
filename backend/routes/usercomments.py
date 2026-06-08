from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.comment import Comment
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter(
    prefix="/modules",
    tags=["Comments"]
)

# =========================
# GET COMMENTS BY MODULE
# =========================
@router.get("/comments/{module_id}", response_model=List[CommentResponse])
def get_module_comments(module_id: int, db: Session = Depends(get_db)):

    comments = db.query(Comment).filter(
        Comment.module_id == module_id
    ).order_by(Comment.created_at.asc()).all()

    return comments

# =========================
# GET COMMENTS BY MODULE id and user id
# =========================
@router.get("/user/{user_id}/module/{module_id}", response_model=list[CommentResponse])
def get_comments_by_user_and_module(
    user_id: int,
    module_id: int,
    db: Session = Depends(get_db)
):
    comments = db.query(Comment).filter(
        Comment.user_id == user_id,
        Comment.module_id == module_id
    ).order_by(Comment.created_at.asc()).all()

    return comments

# =========================
# CREATE COMMENT
# =========================
@router.post("/{module_id}/comments", response_model=CommentResponse)
def create_comment(
    module_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db)
):
    comment = Comment(
        user_id=data.user_id,
        module_id=module_id,
        text=data.text
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# =========================
# UPDATE COMMENT
# =========================
@router.put("/{module_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    module_id: int,
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db)
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.module_id == module_id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.text = data.text

    db.commit()
    db.refresh(comment)

    return comment


# =========================
# DELETE COMMENT
# =========================
@router.delete("/{module_id}/comments/{comment_id}")
def delete_comment(
    module_id: int,
    comment_id: int,
    db: Session = Depends(get_db)
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.module_id == module_id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}