"""Business logic for authorized-student operations within channel modules."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.authorized_student import AuthorizedStudent
from app.models.channel_modules import ChannelModule
from app.repositories import (
    authorized_student_repository,
    channel_repository,
)
from app.services import channel_service


# ---------------- LOOKUPS / ACCESS ----------------
def _get_module_or_404(db: Session, module_id: int) -> ChannelModule:
    """Return a channel module or raise ``404`` when it does not exist."""
    module = channel_repository.get_module_by_id(db, module_id)

    if module is None:
        raise HTTPException(status_code=404, detail="Channel module not found")

    return module


def _get_channel_or_404(db: Session, module: ChannelModule):
    """Return the channel that owns a module or raise ``404``."""
    channel = channel_repository.get_channel_by_id(db, module.channel_id)

    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    return channel


def _module_role(
    channel,
    module: ChannelModule,
    actor_user_id: Optional[int],
    actor_email: Optional[str],
) -> Optional[str]:
    """Return the actor's role for a module, or ``None`` when unauthorized."""
    role = channel_service.get_channel_role(
        channel,
        user_id=actor_user_id,
        email=actor_email,
    )

    if role is not None:
        return role

    # A module can be created by a channel member. The module creator and the
    # module-level co-host are allowed to manage that module's students.
    if actor_user_id is not None and module.user_id == actor_user_id:
        return channel_service.OWNER_ROLE

    if actor_email and module.co_host_email:
        if module.co_host_email.strip().lower() == actor_email.strip().lower():
            return channel_service.CO_HOST_ROLE

    return None


def _require_module_access(
    channel,
    module: ChannelModule,
    actor_user_id: Optional[int],
    actor_email: Optional[str],
) -> Optional[str]:
    """Enforce module access when an actor identity is supplied.

    The legacy client does not send an actor for authorized-student calls, so
    the check is skipped when neither an authenticated user nor an explicit
    actor parameter is available. When an actor is supplied, channel owners,
    channel co-hosts, module creators and module co-hosts are accepted.
    """
    if actor_user_id is None and actor_email is None:
        return None

    role = _module_role(channel, module, actor_user_id, actor_email)

    if role is None:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to manage students for this channel",
        )

    return role


def _get_student_or_404(db: Session, student_id: int) -> AuthorizedStudent:
    """Return an authorized student or raise ``404``."""
    student = authorized_student_repository.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


def _get_student_context(
    db: Session,
    student: AuthorizedStudent,
):
    """Return the module/channel for a student, or ``(None, None)``."""
    module = channel_repository.get_module_by_id(
        db,
        student.channel_module_id,
    )
    channel = (
        channel_repository.get_channel_by_id(db, module.channel_id)
        if module is not None
        else None
    )
    return module, channel


# ---------------- AUTHORIZED-STUDENT OPERATIONS ----------------
def add_student(
    db: Session,
    payload,
    actor_user_id: Optional[int] = None,
    actor_email: Optional[str] = None,
) -> AuthorizedStudent:
    """Authorize a student for a channel module."""
    module = _get_module_or_404(db, payload.channel_module_id)
    channel = _get_channel_or_404(db, module)
    _require_module_access(channel, module, actor_user_id, actor_email)

    existing = authorized_student_repository.get_student_by_module_and_email(
        db,
        module_id=module.module_id,
        student_email=payload.student_email,
    )

    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="Student is already authorized for this module",
        )

    student = AuthorizedStudent(**payload.model_dump())
    return authorized_student_repository.create_student(db, student)


def get_students_by_module(
    db: Session,
    module_id: int,
    actor_user_id: Optional[int] = None,
    actor_email: Optional[str] = None,
):
    """Return the students authorized for a module."""
    module = _get_module_or_404(db, module_id)
    channel = _get_channel_or_404(db, module)
    _require_module_access(channel, module, actor_user_id, actor_email)

    return authorized_student_repository.get_students_by_module(
        db,
        module.module_id,
    )


def get_student(
    db: Session,
    student_id: int,
    actor_user_id: Optional[int] = None,
    actor_email: Optional[str] = None,
) -> AuthorizedStudent:
    """Return a single authorized student."""
    student = _get_student_or_404(db, student_id)
    module, channel = _get_student_context(db, student)

    if module is None:
        raise HTTPException(status_code=404, detail="Channel module not found")

    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    _require_module_access(channel, module, actor_user_id, actor_email)
    return student


def update_student(
    db: Session,
    student_id: int,
    payload,
    actor_user_id: Optional[int] = None,
    actor_email: Optional[str] = None,
) -> AuthorizedStudent:
    """Update an authorized student's status or remark."""
    student = _get_student_or_404(db, student_id)
    module, channel = _get_student_context(db, student)

    if module is None:
        raise HTTPException(status_code=404, detail="Channel module not found")

    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    _require_module_access(channel, module, actor_user_id, actor_email)

    if payload.status is not None:
        student.status = payload.status

    if payload.remark is not None:
        student.remark = payload.remark

    return authorized_student_repository.update_student(db, student)


def delete_student(
    db: Session,
    student_id: int,
    actor_user_id: Optional[int] = None,
    actor_email: Optional[str] = None,
) -> dict:
    """Remove an authorized student.

    When the parent module or channel is already gone the record is treated as
    orphaned and may still be deleted, so stale rows cannot become impossible
    to clean up.
    """
    student = _get_student_or_404(db, student_id)
    module, channel = _get_student_context(db, student)

    if module is not None and channel is not None:
        _require_module_access(channel, module, actor_user_id, actor_email)

    authorized_student_repository.delete_student(db, student)

    return {"message": "Student removed successfully"}
