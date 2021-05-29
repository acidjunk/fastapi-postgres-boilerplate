# fastapi-postgres-boilerplate
My own fastapi postgres boilerplate

## Server

This project only works with Python 3.8, 3.9 and 3.10.
If you want to use a virtual environment first create the environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

You can install the required libraries with pip. The following command will install all the required
libraries for the project. Check out the different files under requirements to more specifically see
which library is used and for what reason.

```shell
pip install -r ./requirements/all.txt
```

A PostgreSQL user and two databases are required ('boilerplate' is the password used by default).

```shell
createuser -sP boilerplate
createdb boilerplate -O boilerplate
createdb boilerplate-test -O boilerplate
```

Now you should be able to start a hot reloading, api server:
```shell
PYTHONPATH=. uvicorn server.main:app --reload --port 8080
```

Or run a threaded server and auto-apply migrations on launch:
```shell
/bin/server
````

## Configuring the server

All configuration is done via ENV vars. 

```shell
export SESSION_SECRET="SUPER_DUPER_SECRET"
export TESTING=False
export TRACING_ENABLED=Treu
```

> Note: FastAPI will detect and automatically load an existing `.env` file. 

## DB Migrations

The database schema is maintained by migrations (see `/migrations` for the
definitions). Pending migrations are automatically applied when starting the
server.

There are 2 migration branches that move independently of one another. The data branch which contains
all needed data (e.g. examples etc.) and the Schema branch.

### Schema migration

To create a new schema migration:

```shell
PYTHONPATH=. alembic revision --autogenerate -m "New schema" --head=schema@head
```

This opens a new migration in `/migrations/version/`

### General Migration

To create a data migration do the following:

```shell
PYTHONPATH=. alembic revision --message "Name of the migration" --head=general@head
```

This will also create a new revision file where normal SQL can be written like so:

```python
conn = op.get_bind()
res = conn.execute("INSERT INTO products VALUES ('x', 'y', 'z')")
```

## Manual deploy

Activate a python env with SAM installed, fire up Docker if it's not already running and run:

```
sam validate
sam build --use-container --debug
sam package --s3-bucket YOUR_S3_BUCKET \
--output-template-file out.yml --region eu-central-1
```

And then deploy it with:

```
sam deploy --template-file out.yml \
--stack-name fastapi-postgres-boilerplate \
--region eu-central-1 --no-fail-on-empty-changeset \
--capabilities CAPABILITY_IAM
```