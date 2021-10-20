from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from server.crud.base import CRUDBase
from server.db import db
from server.db.models import User
from server.schemas.user import UserCreate, UserUpdate
from server.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, *, email: str) -> Optional[User]:
        return User.query.filter(User.email == email).first()

    def get_by_username(self, *, username: str) -> Optional[User]:
        return User.query.filter(User.username == username).first()

    def get(self, id: Optional[str] = None) -> Optional[User]:
        user = User.query.get(id)
        return user

    def create(self, *, obj_in: UserCreate) -> User:
        db_obj = User()
        db.session.add(db_obj)
        db.session.commit()
        # db.commit()
        # db.refresh(db_obj)
        return db_obj

    def update(self, *, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        for field in obj_data:
            if field != "id" and field in update_data:
                setattr(db_obj, field, update_data[field])
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def authenticate(self, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_crud = CRUDUser(User)
