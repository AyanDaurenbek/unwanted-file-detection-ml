.PHONY: up down test lint train fmt

up:
	docker-compose up --build

down:
	docker-compose down

test:
	pytest -q

lint:
	ruff check src tests

fmt:
	black src tests

train:
	python -m src.models.train --config configs/train.yaml
