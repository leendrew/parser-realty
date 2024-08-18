COMPOSE_PATH_DEV := ./compose.dev.yaml
COMPOSE_PATH_PROD := ./compose.prod.yaml
ENV_PATH_DEV := ./.env.development
ENV_PATH_PROD := ./.env.production

compose-dev-build-app:
	docker compose --env-file $(ENV_PATH_DEV) -f $(COMPOSE_PATH_DEV) build app

compose-dev-up-app:
	docker compose --env-file $(ENV_PATH_DEV) -f $(COMPOSE_PATH_DEV) up app -d

compose-dev-build-db:
	docker compose --env-file $(ENV_PATH_DEV) -f $(COMPOSE_PATH_DEV) build db

compose-dev-up-db:
	docker compose --env-file $(ENV_PATH_DEV) -f $(COMPOSE_PATH_DEV) up db -d

compose-prod-build-app:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) build app 

compose-prod-up-app:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) up app -d

compose-prod-build-db:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) build db

compose-prod-up-db:
	docker compose --env-file $(ENV_PATH_PROD) -f $(COMPOSE_PATH_PROD) up db -d

dev-build: compose-dev-build-app compose-dev-build-db

dev-up: compose-dev-up-app compose-dev-up-db

dev-down:
	docker compose -f $(COMPOSE_PATH_DEV) down

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

migration-down-all:
	alembic downgrade all
