install:
	pip3 install -r requirements.txt

test:
	pytest tests

.PHONY: build_run
build_run:
	sudo docker compose up --build

up:
	sudo docker compose up

down:
	sudo docker compose down

clean_docker:
	sudo docker compose down -v --remove-orphans
	sudo docker system prune -af
