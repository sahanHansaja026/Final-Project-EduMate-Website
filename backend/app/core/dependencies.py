from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Optional variant used by endpoints that must stay compatible with clients
# which do not send a bearer token yet. When a valid token is present the
# authenticated user is used for ownership checks; otherwise the endpoint may
# fall back to its explicit actor parameter.
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    auto_error=False,
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the currently authenticated user from the bearer access token.

    The JWT is validated with the shared security utilities (signature, expiry
    and subject) and the user is loaded from the database. Invalid or expired
    tokens, as well as unknown subjects, result in a ``401 Unauthorized``.
    """
    payload = decode_access_token(token)

    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = db.query(User).filter(User.email == payload["sub"]).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    return user


def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Resolve the authenticated user when a bearer token is supplied.

    Returns ``None`` for anonymous requests or invalid tokens so legacy
    endpoints can keep working while still enforcing ownership whenever an
    authenticated identity is available.
    """
    if not token:
        return None

    payload = decode_access_token(token)

    if payload is None or "sub" not in payload:
        return None

    return db.query(User).filter(User.email == payload["sub"]).first()
