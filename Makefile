.PHONY: test lint run frontend
test:; PYTHONPATH=backend pytest backend/tests
lint:; ruff check backend
run:; PYTHONPATH=backend uvicorn app.main:app --reload --port 8080
frontend:; npm --prefix frontend run dev
