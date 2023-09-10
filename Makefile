build:
	docker compose up -d 
	docker exec -t fastapi /opt/pdd/venv/bin/alembic upgrade head

rebuild:
	docker compose up --force-recreate --build -d 

upgradedb:
	docker exec -t fastapi /opt/pdd/venv/bin/alembic upgrade head