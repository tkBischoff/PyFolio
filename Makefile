all:
	docker-compose -f app/docker-compose.yaml up --build --remove-orphans

