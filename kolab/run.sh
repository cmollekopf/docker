#!/bin/bash

source ./config.sh

#Run foreground and remove container when stopped
# docker run --rm -ti -p 80:80 -p 143:143 -p 443:443 -p 587:587 -p 4190:4190 -h $HOSTNAME -v /sys/fs/cgroup:/sys/fs/cgroup:ro $REPONAME:latest

#Run in background (you need to remove the container yourself
docker run -d -p 80:80 -p 143:143 -p 443:443 -p 587:587 -p 4190:4190 -h $HOSTNAME -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $(pwd)/populate:/populate $REPONAME:$TAG
