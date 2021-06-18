from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from server.security import get_password_hash, verify_password
from server.crud.base import CRUDBase
from server.db.models import UsersTable
from server.schemas.user import User, UserCreate, UserUpdate


class CRUDAPIUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(UsersTable).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(UsersTable).filter(User.username == username).first()

    def get(self, db_session: Session, id: Optional[str] = None) -> Optional[User]:
        user = db_session.query(UsersTable).get(id)
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = UsersTable(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        for field in obj_data:
            if field != "id" and field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_crud = CRUDAPIUser(User)
