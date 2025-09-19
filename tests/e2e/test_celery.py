import time
import requests
import pytest


class TestCeleryE2E:
    """End-to-end tests for Celery tasks."""

    @pytest.fixture(scope="class")
    def base_url(self):
        """Base URL for the API."""
        return "http://localhost:8080"

    def test_add_task(self, base_url):
        """Test basic addition task."""
        response = requests.get(f"{base_url}/add?x=5&y=3")
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "queued"
        task_id = data["task_id"]

        # Wait for completion
        time.sleep(3)

        # Check result
        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert result_data["result"] == 8

    def test_multiply_task(self, base_url):
        """Test multiplication task."""
        response = requests.get(f"{base_url}/multiply?x=4&y=6")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(2)

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert result_data["result"] == 24

    def test_divide_task(self, base_url):
        """Test division task."""
        response = requests.get(f"{base_url}/divide?x=10&y=2")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(2)

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert result_data["result"] == 5.0

    def test_divide_by_zero_error(self, base_url):
        """Test division by zero error handling."""
        response = requests.get(f"{base_url}/divide?x=10&y=0")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(2)

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "FAILURE"
        assert "Cannot divide by zero" in result_data["info"]

    def test_long_task_progress(self, base_url):
        """Test long task with progress updates."""
        response = requests.get(f"{base_url}/long_task")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        # Check progress during execution
        time.sleep(2)
        progress_response = requests.get(f"{base_url}/tasks/{task_id}")
        progress_data = progress_response.json()
        # Should be in PROGRESS state
        assert progress_data["status"] in ["PROGRESS", "SUCCESS"]

        # Wait for completion
        time.sleep(6)
        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert result_data["result"] == "Long task completed"

    def test_chain_example(self, base_url):
        """Test task chaining: (x + y) * z."""
        response = requests.get(f"{base_url}/chain_example?x=2&y=3&z=4")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(5)  # Chain takes longer

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert result_data["result"] == 20  # (2+3)*4 = 20

    def test_group_example(self, base_url):
        """Test group task: sum multiple numbers."""
        response = requests.get(f"{base_url}/group_example?numbers=1,2,3,4,5")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(3)

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        # Group returns list of results, sum them
        assert sum(result_data["result"]) == 15  # 1+2+3+4+5 = 15

    def test_callback_example(self, base_url):
        """Test callback task."""
        response = requests.get(f"{base_url}/callback_example?x=5&y=10")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(4)

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert "Processed result: 15" in result_data["result"]

    def test_random_delay_task(self, base_url):
        """Test random delay task."""
        response = requests.get(f"{base_url}/random_delay")
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]

        time.sleep(4)  # Max delay is 3 seconds

        result_response = requests.get(f"{base_url}/tasks/{task_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["status"] == "SUCCESS"
        assert "Delayed for" in result_data["result"]
