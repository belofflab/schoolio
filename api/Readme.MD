1. virtualenv venv 
2. venv/Scripts/activate
3. pip install poetry
4. poetry install

## Create database store-api
5. poetry run alembic upgrade head
6. poetry run fastapi-app