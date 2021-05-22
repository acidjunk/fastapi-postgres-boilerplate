
FROM python:3.8

COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/deploy.txt

EXPOSE 8080

COPY ./server /server
COPY .env-production /.env

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8080"]