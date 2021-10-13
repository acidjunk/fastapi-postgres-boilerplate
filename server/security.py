from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from structlog import get_logger

from server.settings import app_settings
from fastapi_users.authentication import CookieAuthentication

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = get_logger(__name__)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, app_settings.SESSION_SECRET, algorithm=app_settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

cookie_authentication = CookieAuthentication(secret=app_settings.SECRET, lifetime_seconds=3600)