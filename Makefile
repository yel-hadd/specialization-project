# EduTrack Analytics - common tasks
.PHONY: help up down build logs data test seed schema clean

help:
	@echo "Targets:"
	@echo "  make up      - build and start the full stack (Postgres + backend + frontend)"
	@echo "  make down    - stop the stack"
	@echo "  make build   - build the Docker images"
	@echo "  make logs    - follow logs from all services"
	@echo "  make data    - run data/generate_synthetic.py (samples + edge_cases dans data/samples/)"
	@echo "  make test    - run the backend test suite (in the backend container)"
	@echo "  make schema  - export the PostgreSQL schema to backend/schema.sql"
	@echo "  make clean   - stop the stack and remove volumes (drops the database)"

up:
	cp -n .env.example .env || true
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

# Genere les fichiers d'exemple (etudiants.csv, notes.csv, absences.xlsx)
# et les fichiers de test dans data/samples/edge_cases/
data:
	python data/generate_synthetic.py

test:
	docker compose run --rm backend pytest -q

schema:
	docker compose run --rm backend python export_schema.py

clean:
	docker compose down -v
