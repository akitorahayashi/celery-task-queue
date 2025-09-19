import time
import requests
import pytest


def test_add_task():
    """E2E test for adding two numbers asynchronously via Celery."""
    base_url = "http://localhost:8080"

    # Step 1: Enqueue the task
    response = requests.get(f"{base_url}/add?x=5&y=3")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "queued"
    task_id = data["task_id"]

    # Step 2: Wait for the task to complete
    time.sleep(3)  # Wait for Celery to process the task

    # Step 3: Check the task result
    result_response = requests.get(f"{base_url}/tasks/{task_id}")
    assert result_response.status_code == 200
    result_data = result_response.json()
    assert result_data["status"] == "SUCCESS"
    assert result_data["result"] == 8
