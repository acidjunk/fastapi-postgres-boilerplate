from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from server.crud import user_crud
from server.db import db
from server.db.models import UsersTable
from server.schemas import TokenPayload
from server.settings import app_settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/login/access-token")


def get_current_user(token: str = Depends(reusable_oauth2)) -> UsersTable:
    try:
        payload = jwt.decode(
            token, app_settings.SESSION_SECRET, algorithms=[app_settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_crud.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: UsersTable = Depends(get_current_user),
) -> UsersTable:
    if not user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: UsersTable = Depends(get_current_user),
) -> UsersTable:
    if not user_crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
