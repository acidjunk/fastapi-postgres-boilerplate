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
from server.db import ProductsTable
from server.schemas.product import Product, ProductCreate, ProductUpdate
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[Product])
def fetch(product_type: Optional[str] = None) -> List[Product]:
    query = ProductsTable.query

    if product_type:
        query = query.filter(ProductsTable.__dict__["product_type"] == product_type)

    return query.all()


@router.get("/{id}", response_model=Product)
def product_by_id(id: UUID) -> ProductsTable:
    product = ProductsTable.query.filter_by(id=id).first()
    if not product:
        raise_status(HTTPStatus.NOT_FOUND, f"Product id {id} not found")
    return product


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def save_product(data: ProductCreate = Body(...)) -> None:
    logger.info("Saving map", data=data)
    return save(ProductsTable, data)


@router.put("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update_product(data: ProductUpdate = Body(...)) -> None:
    return update(ProductsTable, data)


@router.delete("/{product_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete_product(product_id: UUID) -> None:
    return delete(ProductsTable, product_id)
