COMPOSE_PATH_DEV := ./compose.dev.yaml
COMPOSE_PATH_PROD := ./compose.prod.yaml
ENV_PATH_DEV := ./.env.development
ENV_PATH_PROD := ./.env.production

dev-up-app:
	python3 -m src.main

dev-up-bot:
	python3 -m src.tg_bot.main

compose-prod-build-app:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) build app 

compose-prod-up-app:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) up app -d

compose-prod-build-db:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) build db

compose-prod-up-db:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) up db -d

prod-build: compose-prod-build-app compose-prod-build-db

prod-up: compose-prod-up-app compose-prod-up-db

prod-down:
	docker compose -f $(COMPOSE_PATH_PROD) down

migration-add:
	alembic revision --autogenerate

migration-up:
	alembic upgrade head

migration-down:
	alembic downgrade -1

migration-down-base:
	alembic downgrade base
