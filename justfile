setup:
  [ -f .env ] || cp .env.example .env
  uv sync

dev:
  docker compose up --build -d

format:
	uv run black .
	uv run ruff check . --fix

lint: 
  uv run black --check .
  uv run ruff check .

e2e-test:
  uv sync --group dev
  docker compose up -d
  uv run pytest tests/e2e
  docker compose down

stop:
  docker compose down
