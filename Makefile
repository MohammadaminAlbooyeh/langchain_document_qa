.PHONY: install run-backend run-frontend test lint clean docker-up

install:
	pip install -r requirements.txt

run-backend:
	uvicorn backend.main:app --reload --port 8000

run-frontend:
	cd frontend && npm start

test:
	pytest

lint:
	flake8 backend/
	black --check backend/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf chroma_db/ .pytest_cache/

docker-up:
	docker-compose up

docker-down:
	docker-compose down
