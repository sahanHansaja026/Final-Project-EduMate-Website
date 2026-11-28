"""Database access layer for channel authorized-student operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.authorized_student import AuthorizedStudent


def get_student_by_id(db: Session, student_id: int) -> Optional[AuthorizedStudent]:
    """Return the authorized student with the given primary key or ``None``."""
    return db.query(AuthorizedStudent).filter(
        AuthorizedStudent.id == student_id
    ).first()


def get_students_by_module(db: Session, module_id: int) -> List[AuthorizedStudent]:
    """Return every authorized student enrolled in ``module_id``."""
    return db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == module_id
    ).all()


def get_student_by_module_and_email(
    db: Session,
    module_id: int,
    student_email: str,
) -> Optional[AuthorizedStudent]:
    """Return an existing authorization for a student/module pair."""
    return db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == module_id,
        AuthorizedStudent.student_email == student_email,
    ).first()


def count_students_by_module(db: Session, module_id: int) -> int:
    """Count the authorized students enrolled in ``module_id``."""
    return db.query(AuthorizedStudent).filter(
        AuthorizedStudent.channel_module_id == module_id
    ).count()


def create_student(db: Session, student: AuthorizedStudent) -> AuthorizedStudent:
    """Persist a new authorized student."""
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: AuthorizedStudent) -> AuthorizedStudent:
    """Persist changes applied to an existing authorized student."""
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: AuthorizedStudent) -> None:
    """Remove an authorized student."""
    db.delete(student)
    db.commit()
