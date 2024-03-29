FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install


COPY ./app /app/app
COPY ./alembic/. /app/alembic/.
COPY alembic-db.ini /app/alembic.ini

CMD ["alembic", "upgrade", "head"]

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
