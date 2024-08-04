FROM python:3.11.2-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libpq-dev python3-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install flake8==6.0.0

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

RUN flake8 --ignore=E501,F401,W503
