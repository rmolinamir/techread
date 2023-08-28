build:
	docker compose -f docker/local/compose.yml up --build -d --remove-orphans

up:
	docker compose -f docker/local/compose.yml up -d

down:
	docker compose -f docker/local/compose.yml down

down-volumes:
	docker compose -f docker/local/compose.yml down -v

prune:
	docker system prune -f

logs:
	docker compose -f docker/local/compose.yml logs -f

logs-techread:
	docker compose -f docker/local/compose.yml logs techread

makemigrations:
	docker compose -f docker/local/compose.yml run --rm techread python manage.py makemigrations

migrate:
	docker compose -f docker/local/compose.yml run --rm techread python manage.py migrate

collectstatic:
	docker compose -f docker/local/compose.yml run --rm techread python manage.py collectstatic --noinput

superuser:
	docker compose -f docker/local/compose.yml run --rm techread python manage.py createsuperuser

volume:
	docker volume inspect local_local_postgres_data

techread-db:
	docker compose -f docker/local/compose.yml exec postgres psql -U techread -d techread

lint:
	docker compose -f docker/local/compose.yml exec techread flake8 .

format:
	docker compose -f docker/local/compose.yml exec techread black --exclude=migrations .

format-check:
	docker compose -f docker/local/compose.yml exec techread black --check --exclude=migrations .

format-diff:
	docker compose -f docker/local/compose.yml exec techread black --diff --exclude=migrations .

isort:
	docker compose -f docker/local/compose.yml exec techread isort --skip venv --skip migrations .

isort-check:
	docker compose -f docker/local/compose.yml exec techread isort --check-only --skip venv --skip migrations .

isort-diff:
	docker compose -f docker/local/compose.yml exec techread isort --diff --skip venv --skip migrations .