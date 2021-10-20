from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi_users.models import BaseUser, BaseUserCreate, BaseUserUpdate, BaseUserDB

from pydantic import BaseModel, EmailStr


# Shared properties
class User(BaseUser):
    pass

    class Config:
        orm_mode = True


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(User, BaseUserUpdate):
    pass


class UserDB(User, BaseUserDB):
    pass
