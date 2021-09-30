from typing import Optional

from fastapi.encoders import jsonable_encoder

from server.crud.base import CRUDBase
from server.db import db
from server.db.models import MapsTable
from server.schemas.map import MapCreate, MapUpdate


class CRUDMap(CRUDBase[MapsTable, MapCreate, MapUpdate]):
    pass
    # def create_with_owner(
    #     self, *, obj_in: MapCreate, user_id: str
    # ) -> MapsTable:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, user_id=user_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj


map_crud = CRUDMap(MapsTable)
