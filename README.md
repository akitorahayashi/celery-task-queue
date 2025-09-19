# Celery Queue Sample

A sample application for asynchronous task queues using Celery and Redis.

## Overview

- **Celery**: Asynchronous task queue management
- **Redis**: Message broker and result backend
- **FastAPI**: REST API server

## Setup

1. **Setup environment**:
   ```bash
   just setup
   ```
   This will create `.env` file from `.env.example` if it doesn't exist and install dependencies with `uv sync`.

2. **Start Redis**:
    ```bash
    docker-compose up -d redis
    ```

## How to Run

1. **Start Celery worker**:
   ```bash
   uv run celery -A celery.app worker --loglevel=info
   ```

2. **Start FastAPI server**:
   ```bash
   uv run uvicorn api.main:app --reload
   ```

3. **Using Docker Compose**:
   ```bash
   just dev
   ```
   This will start all services including Redis, Celery worker, and FastAPI server.

## API Usage Examples

Once the server is running, you can test tasks using the following endpoints.

- **Create task**: POST `/tasks/`
  - Request body: `{"message": "Hello World"}`
  - Response: Task ID

- **Get task result**: GET `/tasks/{task_id}`
  - Response: Task status and result

Example:
```bash
curl -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" -d '{"message": "Test task"}'
```

## Troubleshooting

- If Redis is not running: Run `redis-server`
- Port conflicts: Change ports as needed
- Check logs: Review Celery worker and FastAPI logs

## For Developers

- `justfile`: For convenient task execution
  - `just setup`: Setup environment and install dependencies
  - `just dev`: Start all services with Docker Compose
  - `just stop`: Stop all services
- `Dockerfile`: For containerization
- `docker-compose.yml`: For full environment setup
