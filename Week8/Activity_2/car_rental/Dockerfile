# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements (sqlite3 is in stdlib, so this may be empty)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy application source
COPY . /app

CMD ["python", "app.py"]
