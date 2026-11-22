"""Business logic layer for user management."""

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.subscription import PlanEnum, Subscription
from app.repositories import user_repository
from app.schemas.user import LoginSchema, SignupSchema, TokenSchema, UserOut


def signup(signup_data: SignupSchema, db: Session) -> dict:
    """Register a new user and provision the free subscription plan."""
    if user_repository.get_user_by_email(db, signup_data.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user = user_repository.create_user(db, signup_data.email, hash_password(signup_data.password))

    db.add(
        Subscription(
            user_id=user.user_id,
            user_email=user.email,
            plan_name=PlanEnum.free,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            status="active",
        )
    )
    db.commit()

    return {"message": "User registered successfully", "user_id": user.user_id}


def login(login_data: LoginSchema, db: Session) -> TokenSchema:
    """Authenticate a user and issue access/refresh tokens."""
    user = user_repository.get_user_by_email(db, login_data.email)

    if user is None or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    refresh_days = 60 if login_data.remember_me else 30

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email}, days=refresh_days)

    user.refresh_token = refresh_token
    db.commit()

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserOut(id=user.user_id, email=user.email),
    )


def logout(refresh_token: str, db: Session) -> dict:
    """Invalidate the refresh token of a logged out session."""
    user = user_repository.get_user_by_refresh_token(db, refresh_token)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user.refresh_token = None
    db.commit()

    return {"message": "Logged out successfully"}
