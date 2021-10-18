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

from server.api.deps import common_parameters
from server.api.error_handling import raise_status
from server.crud import product_type_crud
from server.db.models import ProductTypesTable
from server.schemas import ProductType, ProductTypeCreate, ProductTypeUpdate

router = APIRouter()


@router.get("/", response_model=List[ProductType])
def get_multi(response: Response, common: dict = Depends(common_parameters)) -> List[ProductType]:
    product_types, header_range = product_type_crud.get_multi(
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
        sort_parameters=common["sort"],
    )
    response.headers["Content-Range"] = header_range
    return product_types


@router.get("/{id}", response_model=ProductType)
def get_by_id(id: UUID) -> ProductTypesTable:
    product_type = product_type_crud.get(id)
    if not product_type:
        raise_status(HTTPStatus.NOT_FOUND, f"ProductType id {id} not found")
    return product_type


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def create(data: ProductTypeCreate = Body(...)) -> None:
    return product_type_crud.create(obj_in=data)


@router.put("/{product_type_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update(*, product_type_id: UUID, item_in: ProductTypeUpdate) -> None:
    product_type = product_type_crud.get(id=product_type_id)
    if not product_type:
        raise HTTPException(status_code=404, detail="ProductType not found")

    product_type = product_type_crud.update(
        db_obj=product_type,
        obj_in=item_in,
    )
    return product_type


@router.delete("/{product_type_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete(product_type_id: UUID) -> None:
    # Todo: check product first
    return product_type_crud.delete(id=product_type_id)
