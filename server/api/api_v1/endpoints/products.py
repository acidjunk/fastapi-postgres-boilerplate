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
from server.crud import product_crud
from server.db.models import ProductsTable
from server.schemas import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/", response_model=List[Product])
def get_multi(response: Response, common: dict = Depends(common_parameters)) -> List[Product]:
    products, header_range = product_crud.get_multi(
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
        sort_parameters=common["sort"],
    )
    response.headers["Content-Range"] = header_range
    return products


@router.get("/{id}", response_model=Product)
def get_by_id(id: UUID) -> ProductsTable:
    product = product_crud.get(id)
    if not product:
        raise_status(HTTPStatus.NOT_FOUND, f"Product id {id} not found")
    return product


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def create(data: ProductCreate = Body(...)) -> None:
    return product_crud.create(obj_in=data)


@router.put("/{product_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update(*, product_id: UUID, item_in: ProductUpdate) -> None:
    product = product_crud.get(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product = product_crud.update(
        db_obj=product,
        obj_in=item_in,
    )
    return product


@router.delete("/{product_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete(product_id: UUID) -> None:
    return product_crud.delete(id=product_id)
