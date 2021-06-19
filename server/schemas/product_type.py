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

from typing import Optional
from uuid import UUID

from server.schemas.base import BoilerplateBaseModel


class ProductTypeBase(BoilerplateBaseModel):
    product_type: str
    description: Optional[str]
    product_type_id: Optional[UUID]

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class ProductTypeCreate(ProductTypeBase):
    pass


# Properties to receive via API on update
class ProductTypeUpdate(ProductTypeBase):
    pass


class ProductTypeInDBBase(ProductTypeBase):
    product_type_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductType(ProductTypeBase):
    pass
