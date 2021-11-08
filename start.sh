#!/bin/bash
if [ -d ".venv" ]; then
    echo "Activating venv found in '.venv/'"
    # shellcheck disable=SC1091
    source .venv/bin/activate
else
    echo "Activating venv found in 'venv/'"
    # shellcheck disable=SC1091
    source venv/bin/activate
fi

# FastAPI will autoload .env so this will only handle other known locations that devs can have
# shellcheck disable=SC2002
if [ -f "env" ]; then
    echo "Loading ENV vars from 'env' file"
    # shellcheck disable=SC2046
    export $(cat env | grep -v ^# | xargs)
fi

if [ "$1" = "dev" ]; then
    echo "Starting auto-reloading webserver"
    PYTHONPATH=. uvicorn server.main:app --reload --port 8080
else
    echo "Starting threaded webserver"
    bin/server
fi
