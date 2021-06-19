import os
import uuid
from contextlib import closing
from typing import Dict, cast

import pytest
import respx
import structlog
from alembic import command
from alembic.config import Config
from fastapi.applications import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from server.api.api_v1.api import api_router
from server.api.error_handling import ProblemDetailException
from server.db import (
    ProductsTable,
    db,
)
from server.db.database import (
    ENGINE_ARGUMENTS,
    SESSION_ARGUMENTS,
    BaseModel,
    DBSessionMiddleware,
    SearchQuery,
)
from server.exception_handlers.generic_exception_handlers import (
    form_error_handler,
    problem_detail_handler,
)
from server.forms import FormException
from server.settings import app_settings
from server.types import UUIDstr
from server.utils.date_utils import nowtz

logger = structlog.getLogger(__name__)

CWI: UUIDstr = "2f47f65a-0911-e511-80d0-005056956c1a"
SURFNET: UUIDstr = "4c237817-e64b-47a3-ba0d-0d57bf263266"


def run_migrations(db_uri: str) -> None:
    """
    Configure the alembic context and run the migrations.

    Each test will start with a clean database. This a heavy operation but ensures that our database is clean and
    tests run within their own context.

    Args:
        db_uri: The database uri configuration to run the migration on.

    Returns:
        None

    """
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    os.environ["DATABASE_URI"] = db_uri
    app_settings.DATABASE_URI = db_uri
    alembic_cfg = Config(file_=os.path.join(path, "../../alembic.ini"))
    alembic_cfg.set_main_option(
        "script_location", os.path.join(path, "../../migrations")
    )
    alembic_cfg.set_main_option(
        "version_locations",
        f"{os.path.join(path, '../../migrations/versions/schema')} {os.path.join(path, '../../migrations/versions/general')}",
    )
    alembic_cfg.set_main_option("sqlalchemy.url", db_uri)
    command.upgrade(alembic_cfg, "heads")


@pytest.fixture(scope="session")
def db_uri(worker_id):
    """
    Ensure each pytest thread has its database.

    When running tests with the -j option make sure each test worker is isolated within its own database.

    Args:
        worker_id: the worker id

    Returns:
        Database uri to be used in the test thread

    """
    database_uri = os.environ.get(
        "DATABASE_URI",
        "postgresql://boilerplate:boilerplate@localhost/boilerplate-test",
    )
    if worker_id == "master":
        # pytest is being run without any workers
        return database_uri
    url = make_url(database_uri)
    url.database = f"{url.database}-{worker_id}"
    return str(url)


@pytest.fixture(scope="session")
def database(db_uri):
    """Create database and run migrations and cleanup afterwards.

    Args:
        db_uri: fixture for providing the application context and an initialized database.

    """
    url = make_url(db_uri)
    db_to_create = url.database
    url.database = "postgres"
    engine = create_engine(url)
    with closing(engine.connect()) as conn:
        conn.execute("COMMIT;")
        conn.execute(f'DROP DATABASE IF EXISTS "{db_to_create}";')
        conn.execute("COMMIT;")
        conn.execute(f'CREATE DATABASE "{db_to_create}";')

    run_migrations(db_uri)
    db.engine = create_engine(db_uri, **ENGINE_ARGUMENTS)

    try:
        yield
    finally:
        db.engine.dispose()
        with closing(engine.connect()) as conn:
            conn.execute("COMMIT;")
            conn.execute(f'DROP DATABASE IF EXISTS "{db_to_create}";')


@pytest.fixture(autouse=True)
def db_session(database):
    """
    Ensure tests are run in a transaction with automatic rollback.

    This implementation creates a connection and transaction before yielding to the test function. Any transactions
    started and committed from within the test will be tied to this outer transaction. From the test function's
    perspective it looks like everything will indeed be committed; allowing for queries on the database to be
    performed to see if functions under test have persisted their changes to the database correctly. However once
    the test function returns this fixture will clean everything up by rolling back the outer transaction; leaving the
    database in a known state (=empty with the exception of what migrations have added as the initial state).

    Args:
        database: fixture for providing an initialized database.

    """
    with closing(db.engine.connect()) as test_connection:
        db.session_factory = sessionmaker(**SESSION_ARGUMENTS, bind=test_connection)
        db.scoped_session = scoped_session(db.session_factory, db._scopefunc)
        BaseModel.set_query(cast(SearchQuery, db.scoped_session.query_property()))

        trans = test_connection.begin()
        try:
            yield
        finally:
            trans.rollback()


@pytest.fixture(scope="session", autouse=True)
def fastapi_app(database, db_uri):
    app = FastAPI(
        title="orchestrator",
        openapi_url="/openapi/openapi.yaml",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        default_response_class=JSONResponse,
    )

    app.include_router(api_router, prefix="/api")
    app.add_middleware(SessionMiddleware, secret_key=app_settings.SESSION_SECRET)
    app.add_middleware(DBSessionMiddleware, database=db)
    origins = app_settings.CORS_ORIGINS.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=app_settings.CORS_ALLOW_METHODS,
        allow_headers=app_settings.CORS_ALLOW_HEADERS,
        expose_headers=app_settings.CORS_EXPOSE_HEADERS,
    )
    app.add_exception_handler(FormException, form_error_handler)
    app.add_exception_handler(ProblemDetailException, problem_detail_handler)

    return app


@pytest.fixture(scope="session")
def test_client(fastapi_app):
    return TestClient(fastapi_app)


@pytest.fixture
def mocked_api():
    with respx.mock(base_url="https://foo.bar") as respx_mock:
        respx_mock.get("/users/", content=[], alias="list_users")
        ...
        yield respx_mock


@pytest.fixture()
def product_1():
    product = ProductsTable(
        name="Product 1", description="Product 1 description", created_at=nowtz()
    )
    db.session.add(product)
    db.session.commit()
    return str(product.id)
