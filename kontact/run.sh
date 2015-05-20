#!/bin/bash

#Local kde install directory
KDEROOT=/opt/devel/kolab

#Setup X11 authorization
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

#assumes the container is running
CONTAINER=$(docker ps -a | grep kolab1:ready | head -n 1 | awk '{ print $1 }')

# docker run --rm -ti -u developer -e DISPLAY=$DISPLAY -e XAUTHORITY=$XAUTH --device=/dev/dri/card0:/dev/dri/card0 -v /tmp/.X11-unix:/tmp/.X11-unix -v $KDEROOT:/opt/kde kontact:latest /bin/bash
docker run --rm -ti --link $CONTAINER:kolab -u developer -e DISPLAY=$DISPLAY -e XAUTHORITY=$XAUTH --device=/dev/dri/card0:/dev/dri/card0 -v /tmp/.X11-unix:/tmp/.X11-unix -v $KDEROOT:/opt/kde kontact:latest /bin/bash
