#!/bin/bash

XSOCKET="/tmp/.X11-unix"
XAUTH="/tmp/.docker.xauth"
touch $XAUTH
xauth nlist $DISPLAY | sed -e "s/^..../ffff/" | xauth -f $XAUTH nmerge -

docker run --rm -ti -u developer --device /dev/dri/card0:/dev/dri/card0 --device /dev/dri/renderD128:/dev/dri/renderD128 --device /dev/dri/controlD64:/dev/dri/controlD64 -e DISPLAY=$DISPLAY -e XAUTHORITY=/tmp/.docker.xauth -v $XAUTH:/tmp/.docker.xauth -v $XSOCKET:/tmp/.X11-unix cmollekopf/kubestandalone:latest /bin/bash
