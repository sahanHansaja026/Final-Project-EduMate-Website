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
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
) -> tuple[int, str]:
    """Resolve the authenticated actor and reject impersonation attempts."""
    if user_id is not None and current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to act on behalf of another user",
        )

    if (
        current_email is not None
        and current_email.strip().lower() != current_user.email.strip().lower()
    ):
        raise HTTPException(
            status_code=403,
            detail="Authenticated user does not match current_email",
        )

    return current_user.user_id, current_user.email


def add_student(
    db: Session,
    payload: AuthorizedStudentCreate,
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
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
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
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
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
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
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
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
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
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
