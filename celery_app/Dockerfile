FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv pip install --system .

COPY . .

CMD ["celery", "-A", "celery_app.app:app", "worker", "--loglevel=info", "--concurrency=4"]