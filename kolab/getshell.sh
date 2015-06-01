#!/bin/bash
source ./config.sh
#assumes the container is running
CONTAINER=$(docker ps | grep $REPONAME:$TAG | head -n 1 | awk '{ print $1 }')
docker exec -i -t $CONTAINER bash
