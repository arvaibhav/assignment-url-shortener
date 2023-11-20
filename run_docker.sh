#!/bin/bash

export APP_ENV=${APP_ENV:-development}

# Function to stop and then start the docker-compose services
restart_docker_compose() {
    docker-compose --env-file $1 down
    docker-compose --env-file $1 up -d
}

if [ "$APP_ENV" == "production" ]; then
    restart_docker_compose .env.production
else
    restart_docker_compose .env.development
fi
