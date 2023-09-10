build:
	docker build -t pdd .
	docker run --name pdd -v /home/pddBezZabot/media:/opt/pdd/media -dp 8090:8000 pdd
rebuild:
	docker kill pdd
	docker rm /pdd
	docker build -t pdd .
	docker run --name pdd -v /home/pddBezZabot/media:/opt/pdd/media -dp 8090:8000 pdd
upgrade:
	docker exec -t pdd /opt/pdd/venv/bin/alembic upgrade head
