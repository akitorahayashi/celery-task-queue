from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from celery import chain, group, chord

from .tasks import (
    add, multiply, divide, long_task, process_result,
    add_numbers, random_delay_task
)
from celery_app.app import app as celery_app

app = FastAPI(title="Async Task Queue Sample")


@app.get("/add")
def enqueue_add(x: int, y: int):
    """Basic addition task."""
    try:
        res = add.delay(x, y)
        return {"task_id": res.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/multiply")
def enqueue_multiply(x: int, y: int):
    """Multiplication task."""
    try:
        res = multiply.delay(x, y)
        return {"task_id": res.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/divide")
def enqueue_divide(x: float, y: float):
    """Division task with error handling."""
    try:
        res = divide.delay(x, y)
        return {"task_id": res.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/long_task")
def enqueue_long_task():
    """Long running task with progress updates."""
    try:
        res = long_task.delay()
        return {"task_id": res.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chain_example")
def enqueue_chain_example(x: int, y: int, z: int):
    """Chain tasks: (x + y) * z"""
    try:
        # Chain: add -> multiply
        res = chain(add.s(x, y), multiply.s(z)).delay()
        return {"task_id": res.id, "status": "queued", "description": f"({x} + {y}) * {z}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/group_example")
def enqueue_group_example(numbers: str):
    """Group task: sum multiple numbers."""
    try:
        # Parse comma-separated numbers
        nums = [int(n.strip()) for n in numbers.split(",")]
        # Group: sum all numbers
        res = group(add_numbers.s([n]) for n in nums).delay()
        return {"task_id": res.id, "status": "queued", "description": f"Sum of {nums}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/callback_example")
def enqueue_callback_example(x: int, y: int):
    """Callback example: add -> process_result"""
    try:
        # Chain with callback
        res = chain(add.s(x, y), process_result.s()).delay()
        return {"task_id": res.id, "status": "queued", "description": f"Add {x}+{y} then process"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/random_delay")
def enqueue_random_delay():
    """Task with random delay."""
    try:
        res = random_delay_task.delay()
        return {"task_id": res.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    """Get task result by ID."""
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"status": "PENDING"}
    elif result.state == "PROGRESS":
        return {"status": "PROGRESS", "progress": result.info}
    elif result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": result.result}
    else:
        return {"status": result.state, "info": str(result.info)}
