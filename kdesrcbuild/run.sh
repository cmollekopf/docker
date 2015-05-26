#!/bin/bash

#Local kde install directory
WORKDIR=/home/chrigi/kdebuild/fedora

docker run --rm -ti --privileged -v $WORKDIR:/work -v $(pwd)/kdesrc-buildrc:/home/kdedev/.kdesrc-buildrc -v $(pwd)/bashrc:/home/kdedev/.bashrc fedora-kdedev -c /bin/bash
