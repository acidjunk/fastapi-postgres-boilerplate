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


class MapBaseSchema(BoilerplateBaseModel):
    id: Optional[UUID]
    name: str
    description: str
    size_x: int
    size_y: int
    status: MapStatus
    created_at: Optional[datetime]
    end_date: Optional[datetime]

    class Config:
        orm_mode = True


class MapSchema(MapBaseSchema):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class MapCRUDSchema(MapBaseSchema):
    pass
