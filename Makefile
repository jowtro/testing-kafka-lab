DOCKER_COMPOSE := docker compose
ifeq (, $(shell command -v $(DOCKER_COMPOSE)))
    DOCKER_COMPOSE := docker-compose
endif

.DEFAULT_GOAL := help
.PHONY: start-kafka stop-kafka help

help:
	@echo "Available commands:"
	@sed -n '/^[a-zA-Z_\-]*:/ {s/://; s/^/  make /; s/$$/\t/p}' $(MAKEFILE_LIST)

start-kafka: # Start Kafka
	$(DOCKER_COMPOSE) -f /home/jowtro/docker_jx/kafka_confluent_recent/docker-compose.yml up -d

stop-kafka: # Stop Kafka
	$(DOCKER_COMPOSE) -f /home/jowtro/docker_jx/kafka_confluent_recent/docker-compose.yml down

log-kafka: # Show logs of the Kafka Docker image
	$(DOCKER_COMPOSE) -f /home/jowtro/docker_jx/kafka_confluent_recent/docker-compose.yml logs

start-consumer: # Start the consumer script
	pipenv run python consumer_test.py

start-producer: # Start the producer script
	pipenv run python producer_test.py