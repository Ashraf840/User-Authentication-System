FROM python:alpine3.18
LABEL maintainer="https://github.com/Ashraf840"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8080

RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
    apk update && apk add libpq && \
    apk add --no-cache postgresql-dev gcc musl-dev && \
    /env/bin/pip install --no-cache-dir -r /requirements.txt && \
    adduser --disabled-password --no-create-home app

ENV PATH="/env/bin:$PATH"

USER app