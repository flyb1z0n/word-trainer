#! /bin/bash

docker-compose -f dev-docker-compose.yml stop
docker-compose -f dev-docker-compose.yml up -d
