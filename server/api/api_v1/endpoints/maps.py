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
from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from starlette.responses import Response

from server.api import deps
from server.api.deps import common_parameters
from server.api.error_handling import raise_status
from server.crud import map_crud
from server.db.models import MapsTable, UsersTable
from server.schemas import Map, MapCreate, MapCreateAdmin, MapUpdate, MapUpdateAdmin

router = APIRouter()


@router.get("/", response_model=List[Map])
def get_multi(response: Response, common: dict = Depends(common_parameters)) -> List[Map]:
    maps, header_range = map_crud.get_multi(
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
        sort_parameters=common["sort"],
    )
    response.headers["Content-Range"] = header_range
    return maps


@router.get("/{id}", response_model=Map)
def get_by_id(id: UUID) -> MapsTable:
    map = map_crud.get(id)
    if not map:
        raise_status(HTTPStatus.NOT_FOUND, f"Map id {id} not found")
    return map


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def create(data: MapCreate = Body(...), current_user: UsersTable = Depends(deps.get_current_active_user)) -> None:
    return map_crud.create_with_owner(obj_in=data, created_by=current_user.id)


@router.post("/admin", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def admin_create(
    data: MapCreateAdmin = Body(...), current_user: UsersTable = Depends(deps.get_current_active_superuser)
) -> None:
    return map_crud.create(obj_in=data)


@router.put("/{map_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update(
    *, map_id: UUID, item_in: MapUpdate, current_user: UsersTable = Depends(deps.get_current_active_user)
) -> None:
    map = map_crud.get(id=map_id)
    if not map:
        raise HTTPException(status_code=404, detail="Map not found")
    if str(map.created_by) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You are not authorized to edit this map")

    map = map_crud.update(
        db_obj=map,
        obj_in=item_in,
    )
    return map


@router.put("/admin/{map_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def admin_update(
    *, map_id: UUID, item_in: MapUpdateAdmin, current_user: UsersTable = Depends(deps.get_current_active_superuser)
) -> None:
    map = map_crud.get(id=map_id)
    if not map:
        raise HTTPException(status_code=404, detail="Map not found")

    map = map_crud.update(
        db_obj=map,
        obj_in=item_in,
    )
    return map


@router.delete("/{map_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete(map_id: UUID) -> None:
    return map_crud.delete(id=map_id)
