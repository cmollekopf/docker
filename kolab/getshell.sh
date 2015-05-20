#!/bin/bash
#assumes the container is running
CONTAINER=$(docker ps -a | grep kolab1:ready | head -n 1 | awk '{ print $1 }')
docker exec -i -t $CONTAINER bash
