.PHONY: up down backup lint

up:
	docker-compose -f docker/docker-compose.yml up -d

down:
	docker-compose -f docker/docker-compose.yml down

backup:
	./scripts/backup.sh

lint:
	flake8 || true
