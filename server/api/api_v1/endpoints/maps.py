# Copyright 2019-2020 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi.param_functions import Body
from fastapi.routing import APIRouter

from server.api.error_handling import raise_status
from server.api.models import delete, save, update
from server.db.models import MapsTable
from server.schemas import Map, MapCreate, MapUpdate

router = APIRouter()


@router.get("/", response_model=List[Map])
def fetch(status: Optional[str] = None) -> List[Map]:
    query = MapsTable.query

    if status:
        query = query.filter(MapsTable.__dict__["status"] == status)

    return query.all()


@router.get("/{id}", response_model=Map)
def map_by_id(id: UUID) -> MapsTable:
    map = MapsTable.query.filter_by(id=id).first()
    if not map:
        raise_status(HTTPStatus.NOT_FOUND, f"Map id {id} not found")
    return map


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def save_map(data: MapCreate = Body(...)) -> None:
    return save(MapsTable, data)


@router.put("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update_map(data: MapUpdate = Body(...)) -> None:
    return update(MapsTable, data)


@router.delete("/{map_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete_map(map_id: UUID) -> None:
    return delete(MapsTable, map_id)
