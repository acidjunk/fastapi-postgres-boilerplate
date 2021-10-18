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

"""Module that implements process related API endpoints."""

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from server.api.api_v1.endpoints import health, login, maps, product_types, products, settings, users

# Todo: add security depends here or in endpoints

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])

api_router.include_router(maps.router, prefix="/maps", tags=["maps"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    product_types.router,
    prefix="/product_types",
    tags=["products"],
)
api_router.include_router(settings.router, prefix="/settings", tags=["system"])
api_router.include_router(health.router, prefix="/health", tags=["system"])

api_router.include_router(users.router, prefix="/users", tags=["users"])
