from datetime import timedelta
from http import HTTPStatus
from http.client import HTTPException
from typing import Optional, Any
from uuid import uuid4

import pytest
from server import security
from server.crud import user_crud
from server.db.models import UsersTable
from server.security import verify_password


def login_access_token(username: str, password: str) -> Any:
    user = user_crud.authenticate(username=username, password=password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_crud.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=30)
    return security.create_access_token(user.id, expires_delta=access_token_expires)


def test_users_get_multi_admin(user_admin, test_client):
    token = "Bearer " + login_access_token(username='Admin', password='admin')
    response = test_client.get("/api/users", headers={"Authorization": token})
    assert HTTPStatus.OK == response.status_code
    users = response.json()

    assert 1 == len(users)


def test_users_get_multi_non_admin(user_non_admin, test_client):
    token = "Bearer " + login_access_token(username='User', password='user')
    response = test_client.get("/api/users", headers={"Authorization": token})
    # Isn't it 403 Unauthorized a better response code here ? Currently 400 Bad Request
    assert HTTPStatus.BAD_REQUEST == response.status_code
