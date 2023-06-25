#!/bin/sh

if [ $# -eq 0 ]; then
    docker ps
    exit 1
fi
docker_id=$(docker ps -aqf "name=^$1$")
docker exec -it "$docker_id" /bin/sh
