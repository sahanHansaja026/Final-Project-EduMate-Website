from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.auth import SignupSchema, LoginSchema, TokenSchema
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------- SIGNUP ----------------
@router.post("/signup", status_code=201)
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# ---------------- LOGIN ----------------
@router.post("/login", response_model=TokenSchema)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_days = 60 if data.remember_me else 30

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email}, days=refresh_days)

    # Save refresh token in DB
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# ---------------- LOGOUT ----------------
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.refresh_token == refresh_token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    user.refresh_token = None
    db.commit()

    return {"message": "Logged out successfully"}
