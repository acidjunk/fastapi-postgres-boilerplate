from typing import Optional

from fastapi.encoders import jsonable_encoder

from server.crud.base import CRUDBase
from server.db import db
from server.db.models import MapsTable
from server.schemas.map import MapCreate, MapUpdate


class CRUDMap(CRUDBase[MapsTable, MapCreate, MapUpdate]):
    def create_with_owner(self, *, obj_in: MapCreate, created_by: str) -> MapsTable:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_by=created_by)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj


map_crud = CRUDMap(MapsTable)
