FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY main.py models.py requirements.txt ./
COPY templates/ ./templates/


RUN pip install --no-cache-dir --upgrade -r requirements.txt

