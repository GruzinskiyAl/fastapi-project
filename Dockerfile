FROM python:3.9.6-slim-buster

RUN apt update -y && \
    apt install -y \
    curl && \
    rm -rf /var/lib/apt/lists/*


ENV PROJECT_ROOT=/home/ubuntu/fastapi-app
WORKDIR $PROJECT_ROOT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app $PROJECT_ROOT/app
