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
import databases
import sqlalchemy

from server.db.database import Database, transactional
from server.db.models import ProductsTable  # noqa: F401
from server.db.models import (MapsTable, ProductTypesTable, UtcTimestamp,
                              UtcTimestampException)
from server.settings import app_settings
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


db = Database(app_settings.DATABASE_URI)

dbdatabase = databases.Database(app_settings.DATABASE_URI)

Base: DeclarativeMeta = declarative_base()

engine = sqlalchemy.create_engine(
    app_settings.DATABASE_URI
)
Base.metadata.create_all(engine)

__all__ = [
    "transactional",
    "ProductsTable",
    "ProductTypesTable",
    "MapsTable" "UtcTimestamp",
    "UtcTimestampException",
    "db",
]
