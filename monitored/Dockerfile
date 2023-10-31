FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt mem_cons_tool.py .env ./
COPY mem_cons_tool/ ./mem_cons_tool/


RUN pip install --no-cache-dir --upgrade -r requirements.txt

