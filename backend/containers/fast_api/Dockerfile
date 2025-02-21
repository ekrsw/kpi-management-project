FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY migrations/ migrations/
COPY alembic.ini .

CMD uvicorn src.main:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000} --reload
