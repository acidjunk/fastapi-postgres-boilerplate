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
from typing import List

# from opentelemetry.exporter import jaeger
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    TESTING: bool = True
    SESSION_SECRET: str = "".join(secrets.choice(string.ascii_letters) for i in range(16))  # noqa: S311
    OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM = "HS256"
    CORS_ORIGINS: str = "*"
    CORS_ALLOW_METHODS: List[str] = ["GET", "PUT", "PATCH", "POST", "DELETE", "OPTIONS", "HEAD"]
    CORS_ALLOW_HEADERS: List[str] = ["If-None-Match", "Authorization", "If-Match", "Content-Type"]
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
    DATABASE_URI: str = "postgresql://fastapi:fastapi@localhost/boilerplate"
    MAX_WORKERS: int = 5
    MAIL_SERVER: str = "localhost"
    MAIL_PORT: int = 25
    MAIL_STARTTLS: bool = False
    CACHE_HOST: str = "127.0.0.1"
    CACHE_PORT: int = 6379
    POST_MORTEM_DEBUGGER: str = ""
    SERVICE_NAME: str = "Boilerplate"
    LOGGING_HOST: str = "localhost"
    LOG_LEVEL: str = "DEBUG"
    TRACING_ENABLED: bool = False
    TRACING_INSTRUMENTATION_ENABLED: bool = False
    TRACE_SAMPLE_RATE: float = 1


app_settings = AppSettings()

# # Tracer settings
# jaeger_exporter = jaeger.JaegerSpanExporter(
#     service_name=app_settings.SERVICE_NAME,
#     agent_host_name=app_settings.LOGGING_HOST,
#     insecure=True,
# )
#
# tracer_provider = TracerProvider()
# tracer_provider.add_span_processor(BatchExportSpanProcessor(jaeger_exporter))
