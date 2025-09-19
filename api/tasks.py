import time
import random
from typing import Dict, Any

from celery_app.app import app


@app.task
def add(x: int, y: int) -> int:
    """Basic addition task."""
    time.sleep(2)
    return x + y


@app.task
def multiply(x: int, y: int) -> int:
    """Multiplication task."""
    time.sleep(1)
    return x * y


@app.task
def divide(x: float, y: float) -> float:
    """Division task with error handling."""
    time.sleep(1)
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y


@app.task(bind=True)
def long_task(self) -> str:
    """Long running task with progress updates."""
    total = 10
    for i in range(total):
        time.sleep(0.5)
        self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': total})
    return "Long task completed"


@app.task
def process_result(result: Any) -> str:
    """Callback task to process results."""
    return f"Processed result: {result}"


@app.task
def add_numbers(numbers: list) -> int:
    """Task to sum a list of numbers."""
    time.sleep(1)
    return sum(numbers)


@app.task
def random_delay_task() -> str:
    """Task with random delay."""
    delay = random.uniform(1, 3)
    time.sleep(delay)
    return f"Delayed for {delay:.2f} seconds"
