#!/bin/sh
doc_str="Usage: ./docker.sh image_name [arguments]
    description: run docker image with /bin/sh
    image_name: docker image name
    arguments: all arguments, default is None
    example: ./docker.sh nuclei
             ./docker.sh naabu
             ./docker.sh katana
             ./docker.sh subfinder
"

if [ $# -eq 0 ]; then
    docker ps
    echo "$doc_str"
    exit 1
elif [ "$1" = "-h" ]; then
    docker ps
    echo "$doc_str"
    exit 1
fi

image_name=$(docker images | grep "$1" | head -n1 | awk '{print $1}')
docker_id=$(docker ps -aqf "ancestor=$image_name" | head -n 1)
docker exec -it "$docker_id" /bin/sh -c "cd /root && pwd && ls -la && /bin/sh"
