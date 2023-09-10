# Quick Setup

1. docker-compose up -d 
2. docker exec -t fastapi /opt/pdd/venv/bin/alembic upgrade head

## To rebuild use:
1. docker-compose up --force-recreate --build -d 