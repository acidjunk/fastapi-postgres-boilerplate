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

from fastapi.param_functions import Body
from fastapi.routing import APIRouter

from server.api.error_handling import raise_status
from server.api.models import delete, save, update
from server.db import ProductTypesTable
from server.schemas import ProductTypeBaseSchema, ProductTypeSchema

router = APIRouter()


@router.get("/", response_model=List[ProductTypeSchema])
def fetch() -> List[ProductTypeSchema]:
    return ProductTypesTable.query.all()


@router.get("/{id}", response_model=ProductTypeSchema)
def product_type_by_id(id: UUID) -> ProductTypeSchema:
    product_type = ProductTypesTable.query.filter_by(id=id).first()
    if not product_type:
        raise_status(HTTPStatus.NOT_FOUND, f"Product type {id} not found")
    return product_type


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def save_product_type(data: ProductTypeBaseSchema = Body(...)) -> None:
    return save(ProductTypesTable, data)


@router.put("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update_product_type(data: ProductTypeSchema = Body(...)) -> None:
    return update(ProductTypesTable, data)


@router.delete("/{id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete_product_type(id: UUID) -> None:
    # Todo: check product first
    return delete(ProductTypesTable, id)
