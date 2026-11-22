"""HTTP handling layer for authorized-student operations."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.authorized_student import (
    AuthorizedStudentCreate,
    AuthorizedStudentUpdate,
)
from app.services import authorized_student_service


def _resolve_actor(
    current_user: Optional[User],
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
) -> tuple[Optional[int], Optional[str]]:
    """Resolve the acting identity, preferring the authenticated user."""
    if current_user is not None:
        if user_id is not None and current_user.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to act on behalf of another user",
            )
        return current_user.user_id, current_user.email

    return user_id, current_email


def add_student(
    db: Session,
    payload: AuthorizedStudentCreate,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    current_user: Optional[User] = None,
):
    """Authorize a student for a channel module."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    return authorized_student_service.add_student(
        db,
        payload=payload,
        actor_user_id=actor_user_id,
        actor_email=actor_email,
    )


def get_students_by_module(
    db: Session,
    module_id: int,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    current_user: Optional[User] = None,
):
    """Return the students authorized for a module."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    return authorized_student_service.get_students_by_module(
        db,
        module_id=module_id,
        actor_user_id=actor_user_id,
        actor_email=actor_email,
    )


def get_student(
    db: Session,
    student_id: int,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    current_user: Optional[User] = None,
):
    """Return a single authorized student."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    return authorized_student_service.get_student(
        db,
        student_id=student_id,
        actor_user_id=actor_user_id,
        actor_email=actor_email,
    )


def update_student(
    db: Session,
    student_id: int,
    payload: AuthorizedStudentUpdate,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    current_user: Optional[User] = None,
):
    """Update an authorized student's status or remark."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    return authorized_student_service.update_student(
        db,
        student_id=student_id,
        payload=payload,
        actor_user_id=actor_user_id,
        actor_email=actor_email,
    )


def delete_student(
    db: Session,
    student_id: int,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    current_user: Optional[User] = None,
) -> dict:
    """Remove an authorized student."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    return authorized_student_service.delete_student(
        db,
        student_id=student_id,
        actor_user_id=actor_user_id,
        actor_email=actor_email,
    )
