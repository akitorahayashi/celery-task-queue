# Celery Queue Sample

A sample application for asynchronous task queues.

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
   uv run celery -A celery_app.app worker --loglevel=info
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

Once the server is running, you can test various Celery features using the following endpoints.

### Basic Tasks
- **Addition**: GET `/add?x=5&y=3`
  - Response: `{"task_id": "...", "status": "queued"}`

- **Multiplication**: GET `/multiply?x=4&y=6`
  - Response: `{"task_id": "...", "status": "queued"}`

- **Division**: GET `/divide?x=10&y=2`
  - Response: `{"task_id": "...", "status": "queued"}`

- **Random Delay**: GET `/random_delay`
  - Response: `{"task_id": "...", "status": "queued"}`

### Advanced Features
- **Long Task with Progress**: GET `/long_task`
  - Shows progress updates during execution

- **Task Chain**: GET `/chain_example?x=2&y=3&z=4`
  - Chains tasks: `(2 + 3) * 4 = 20`

- **Group Task**: GET `/group_example?numbers=1,2,3,4,5`
  - Sums multiple numbers using a single task

- **Callback Example**: GET `/callback_example?x=5&y=10`
  - Adds numbers then processes the result

### Task Results
- **Get Task Result**: GET `/tasks/{task_id}`
  - Response examples:
    - `{"status": "PENDING"}`
    - `{"status": "PROGRESS", "progress": {"current": 5, "total": 10}}`
    - `{"status": "SUCCESS", "result": 8}`
    - `{"status": "FAILURE", "info": "Error message"}`

### Example Usage
```bash
# Basic addition
curl "http://localhost:8080/add?x=5&y=3"

# Get result (replace with actual task_id)
curl "http://localhost:8080/tasks/your-task-id-here"

# Task chain
curl "http://localhost:8080/chain_example?x=2&y=3&z=4"

# Group task
curl "http://localhost:8080/group_example?numbers=1,2,3,4,5"
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
