#!/bin/bash
source ./config.sh
#assumes the container is running
CONTAINER=$(docker ps -a | grep $REPONAME:latest | head -n 1 | awk '{ print $1 }')
docker exec -i -t $CONTAINER bash
