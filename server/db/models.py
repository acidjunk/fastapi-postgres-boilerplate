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

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import pytz
import sqlalchemy
import structlog
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Text,
                        TypeDecorator, text, DateTime)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Dialect
from sqlalchemy.exc import DontWrapMixin
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.sql.functions import func

from server.db.database import BaseModel
from server.utils.date_utils import nowtz

logger = structlog.get_logger(__name__)

TAG_LENGTH = 20
STATUS_LENGTH = 255


class UtcTimestampException(Exception, DontWrapMixin):
    pass


class UtcTimestamp(TypeDecorator):
    """Timestamps in UTC.

    This column type always returns timestamps with the UTC timezone, regardless of the database/connection time zone
    configuration. It also guards against accidentally trying to store Python naive timestamps (those without a time
    zone).
    """

    impl = sqlalchemy.types.TIMESTAMP(timezone=True)

    def process_bind_param(
        self, value: Optional[datetime], dialect: Dialect
    ) -> Optional[datetime]:
        if value is not None:
            if value.tzinfo is None:
                raise UtcTimestampException(
                    f"Expected timestamp with tzinfo. Got naive timestamp {value!r} instead"
                )
        return value

    def process_result_value(
        self, value: Optional[datetime], dialect: Dialect
    ) -> Optional[datetime]:
        if value is not None:
            return value.astimezone(timezone.utc)
        return value


class RolesUsersTabke(BaseModel):
    __tablename__ = "roles_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))


class RolesTable(BaseModel):
    __tablename__ = "roles"

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(
        UtcTimestamp, nullable=False, server_default=text("current_timestamp()")
    )
    updated_at = Column(
        UtcTimestamp,
        default=datetime.now(tz=pytz.utc),
        onupdate=datetime.now(tz=pytz.utc),
    )


class User(BaseModel, SQLAlchemyBaseUserTable):
    __tablename__ = "users"

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"


class ProductsTable(BaseModel):
    __tablename__ = "products"

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    description = Column(Text(), nullable=False)
    created_at = Column(
        UtcTimestamp, nullable=False, server_default=text("current_timestamp()")
    )


class ProductTypesTable(BaseModel):
    __tablename__ = "product_types"

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    product_type = Column(String(510), nullable=False, unique=True)
    description = Column(Text())


class MapsTable(BaseModel):
    __tablename__ = "maps"
    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String(510), nullable=False, unique=True)
    description = Column(Text())
    size_x = Column(Integer, default=100)
    size_y = Column(Integer, default=100)
    status = Column(String(255), nullable=False, default="new")
    created_at = Column(
        UtcTimestamp, nullable=False, server_default=text("current_timestamp()")
    )
    updated_at = Column(
        UtcTimestamp,
        server_default=text("current_timestamp()"),
        onupdate=nowtz,
        nullable=False,
    )