.PHONY: all ci ruff run_docker docker_up docker_down clean

SHELL:=/bin/bash
RUN=poetry run
PYTHON=${RUN} python

all:
	@echo "make ci"
	@echo "    Create ci environment."
	@echo "make format"
	@echo "    Format all files using Black."
	@echo "make ruff"
	@echo "    Run 'ruff' to lint project."
	@echo "make run_docker"
	@echo "    Run development web-server using the docker image."
	@echo "make docker_up"
	@echo "    Starts all docker-compose services, except web."
	@echo "make docker_down"
	@echo "    Stop all docker-compose services."
	@echo "make clean"
	@echo "    Remove python artifacts and virtualenv"

ci:
	poetry install --with ci

format:
	${RUN} black .

ruff: ci
	${RUN} ruff check .

run_docker: ci
	docker compose --profile web up --build --attach web

docker_up:
	docker compose --profile db up --build -d

docker_down:
	docker compose --profile web up down

docker_build:
	docker build -t apartment-scraper .

clean:
	poetry env remove --all
	find -type d | grep __pycache__ | xargs rm -rf
	find -type d | grep .*_cache | xargs rm -rf
	rm -rf *.eggs *.egg-info dist build docs/_build .cache .mypy_cache coverage/*
	rm requirements.txt
