THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY : help up down build build-no-cache products-consumer products-producer product-count-consumer product-count-producer create-migrations destroy-migrations appshell dbshell rabbitmqshell db-logs app-logs rabbitmq-logs

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.DEFAULT_GOAL := help

.git/hooks/pre-commit:  # Install git pre-commit hook
	pip install pre-commit
	pre-commit install

up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

products-consumer:
	docker-compose exec dasy sh -c "dasy -r products"

products-producer:
	docker-compose exec dasy sh -c "dasy -w ./data/products.csv"

product-count-consumer:
	docker-compose exec dasy sh -c "dasy -r product_count"

product-count-producer:
	docker-compose exec dasy sh -c "dasy -w product_count"

create-migrations:
	docker-compose exec dasy sh -c "dasy -m forward"

destroy-migrations:
	docker-compose exec dasy sh -c "dasy -m backward"

dbshell:
	docker-compose exec db /bin/bash

appshell:
	docker-compose exec dasy /bin/bash

rabbitmqshell:
	docker-compose exec rabbitmq /bin/bash

db-logs:
	docker-compose logs db

app-logs:
	docker-compose logs dasy

rabbitmq-logs:
	docker-compose logs rabbitmq

pytest:
	docker-compose exec dasy sh -c "pytest -vv"