from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    created_at: datetime
    updated_at: datetime


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
