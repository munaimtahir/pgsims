.PHONY: help dev test up down logs shell migrate makemigrations seed collectstatic clean build restart

help:
	@echo "SIMS Makefile Commands"
	@echo "======================"
	@echo "make dev          - Start development server locally"
	@echo "make test         - Run tests with coverage"
	@echo "make up           - Start all Docker services"
	@echo "make down         - Stop all Docker services"
	@echo "make logs         - View logs from all services"
	@echo "make shell        - Open Django shell"
	@echo "make migrate      - Run database migrations"
	@echo "make makemigrations - Create new migrations"
	@echo "make seed         - Seed database with demo data"
	@echo "make collectstatic - Collect static files"
	@echo "make clean        - Clean Python cache and build files"
	@echo "make build        - Build Docker images"
	@echo "make restart      - Restart Docker services"

dev:
	python manage.py runserver 0.0.0.0:8000

test:
	pytest --cov=sims --cov-report=html --cov-report=term-missing --maxfail=5 -v

up:
	docker-compose up -d
	@echo "Waiting for services to be healthy..."
	@sleep 5
	docker-compose logs web | tail -20

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

seed:
	docker-compose exec web python manage.py sims_seed_demo

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov .pytest_cache .coverage

build:
	docker-compose build --no-cache

restart:
	docker-compose restart

# Production deployment helpers
deploy-check:
	python manage.py check --deploy

deploy-migrate:
	docker-compose exec web python manage.py migrate --noinput

deploy-collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput --clear

deploy-restart:
	docker-compose restart web worker beat
