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

from aiocache import Cache
from fastapi.routing import APIRouter
from starlette.background import BackgroundTasks

from server.settings import app_settings

router = APIRouter()


@router.delete("/cache/{name}", status_code=HTTPStatus.NO_CONTENT)
async def clear_cache(name: str, background_tasks: BackgroundTasks) -> None:
    cache = Cache(Cache.REDIS, endpoint=app_settings.CACHE_HOST, port=app_settings.CACHE_PORT)
    if name == "all":
        background_tasks.add_task(cache.delete, "/*")
    else:
        background_tasks.add_task(cache.delete, f"/{name}*")
