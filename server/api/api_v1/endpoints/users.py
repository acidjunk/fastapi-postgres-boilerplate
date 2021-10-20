from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase

from server.crud.base import get_user_db
from server.schemas.user import User, UserCreate, UserDB, UserUpdate

from fastapi.routing import APIRouter

SECRET = "SECRET"
router = APIRouter()


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def after_verification_request(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
)

# jwt_authentication: JWTAuthentication = JWTAuthentication(
#     secret=settings.SECRET_KEY,
#     lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
# )

fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)


@router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
  return {"message": f"Hello {user.email}!"}