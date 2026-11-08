from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    remember_me: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    email: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserOut

