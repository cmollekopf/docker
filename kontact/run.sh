#!/bin/bash

source ../kolab/config.sh

#Local kde install directory
# KDEROOT=/opt/devel/kolab
KDEROOT=~/kdebuild/fedora/install

#Setup X11 authorization
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

#assumes the container is running
CONTAINER=$(docker ps | grep $REPONAME:$TAG | head -n 1 | awk '{ print $1 }')

# docker run --rm -ti -u developer -e DISPLAY=$DISPLAY -e XAUTHORITY=$XAUTH --device=/dev/dri/card0:/dev/dri/card0 -v /tmp/.X11-unix:/tmp/.X11-unix -v $KDEROOT:/opt/kde kontact:latest /bin/bash
docker run --rm -ti --link $CONTAINER:kolab -u developer -e DISPLAY=$DISPLAY -e XAUTHORITY=$XAUTH --device=/dev/dri/card0:/dev/dri/card0 -v $XAUTH:$XAUTH -v /tmp/.X11-unix:/tmp/.X11-unix -v $KDEROOT:/opt/kde kontact:latest /bin/bash
