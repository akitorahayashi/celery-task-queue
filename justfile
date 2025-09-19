setup:
  [ -f .env ] || cp .env.example .env
  uv sync

dev:
  docker compose up --build -d

format:
	uv run black .
	uv run ruff check . --fix

lint: ## Perform static code analysis (check) using Black and Ruff
  uv run black --check .
  uv run ruff check .

e2e-test:
  uv run pytest tests/e2e

stop:
  docker compose down
