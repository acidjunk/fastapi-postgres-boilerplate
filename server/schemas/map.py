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

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from server.schemas.base import BoilerplateBaseModel
from server.types import strEnum


class MapStatus(strEnum):
    NEW = "new"
    CLOSED = "closed"
    ACTIVE = "active"
    TERMINATED = "terminated"


# Todo: investigate if we need our own Base or just use pydantic's
class MapBase(BoilerplateBaseModel):
    name: str
    description: str
    size_x: int
    size_y: int
    status: MapStatus

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class MapCreate(MapBase):
    pass


class MapCreateAdmin(MapCreate):
    created_by: Optional[UUID]


# Properties to receive via API on update
class MapUpdate(MapBase):
    end_date: Optional[datetime]


class MapUpdateAdmin(MapUpdate):
    created_by: Optional[UUID]


class MapInDBBase(MapBase):
    id: UUID
    created_at: datetime
    created_by: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Map(MapInDBBase):
    pass
