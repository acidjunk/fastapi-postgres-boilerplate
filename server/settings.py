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

import secrets
import string
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, validator
from pydantic.networks import EmailStr, PostgresDsn


class AppSettings(BaseSettings):
    """
    Deal with global app settings.

    The goal is to provide some sensible default for developers here. All constants can be
    overloaded via ENV vars. The validators are used to ensure that you get readable error
    messages when an ENV var isn't correctly formated; for example when you provide an incorrect
    formatted DATABASE_URI.

    ".env" loading is also supported. FastAPI will autoload and ".env" file if one can be found

    In production you need to provide a lot stuff via the ENV. At least DATABASE_URI, SESSION_SECRET,
    TESTING, LOGLEVEL and EMAILS_ENABLED + mail server settings if needed.
    """

    PROJECT_NAME: str = "Boilerplate webservice"
    TESTING: bool = True
    EMAILS_ENABLED: bool = False
    SECRET = "SECRET"
    SESSION_SECRET: str = "".join(
        secrets.choice(string.ascii_letters) for i in range(16)
    )  # noqa: S311
    # OAUTH settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM = "HS256"
    # CORS settings
    CORS_ORIGINS: str = "*"
    CORS_ALLOW_METHODS: List[str] = [
        "GET",
        "PUT",
        "PATCH",
        "POST",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ]
    CORS_ALLOW_HEADERS: List[str] = [
        "If-None-Match",
        "Authorization",
        "If-Match",
        "Content-Type",
    ]
    CORS_EXPOSE_HEADERS: List[str] = [
        "Cache-Control",
        "Content-Language",
        "Content-Length",
        "Content-Type",
        "Expires",
        "Last-Modified",
        "Pragma",
        "Content-Range",
        "ETag",
    ]
    SWAGGER_PORT: int = 8080
    ENVIRONMENT: str = "local"
    SWAGGER_HOST: str = "localhost"
    GUI_URI: str = "http://localhost:3000"
    # DB (probably only postgres for now; we use UUID postgres dialect for the ID's)
    DATABASE_URI: str = "postgresql://boilerplate:boilerplate@localhost/boilerplate"

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    MAX_WORKERS: int = 5
    CACHE_HOST: str = "127.0.0.1"
    CACHE_PORT: int = 6379
    POST_MORTEM_DEBUGGER: str = ""
    SERVICE_NAME: str = "Boilerplate"
    LOGGING_HOST: str = "localhost"
    LOG_LEVEL: str = "DEBUG"

    # Mail settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    FIRST_SUPERUSER = "admin@banaan.org"
    FIRST_SUPERUSER_PASSWORD = "CHANGEME"

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # Todo: check path. The original had one extra folder "app"
    EMAIL_TEMPLATES_DIR: str = "/server/email-templates/build"

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    class Config:
        env_file = ".env"


app_settings = AppSettings()
