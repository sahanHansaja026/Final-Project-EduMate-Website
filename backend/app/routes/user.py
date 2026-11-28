"""User management endpoints (authentication + account management)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import user_controller
from app.core.database import get_db
from app.schemas.user import LoginSchema, SignupSchema, TokenSchema

router = APIRouter()


# ---------------- AUTHENTICATION / USER ACCOUNT ----------------
@router.post("/auth/signup", status_code=201, tags=["Auth"])
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    """Register a new user and provision the free subscription plan."""
    return user_controller.signup(data, db)


@router.post("/auth/login", response_model=TokenSchema, tags=["Auth"])
def login(data: LoginSchema, db: Session = Depends(get_db)):
    """Authenticate a user and return access/refresh tokens."""
    return user_controller.login(data, db)


@router.post("/auth/logout", tags=["Auth"])
def logout(refresh_token: str, db: Session = Depends(get_db)):
    """Invalidate the refresh token of a logged out session."""
    return user_controller.logout(refresh_token, db)
