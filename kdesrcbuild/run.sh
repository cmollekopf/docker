#!/bin/bash

#Local kde install directory
WORKDIR=/home/chrigi/kdebuild/fedora

# docker run --rm -ti --privileged -v $WORKDIR:/work -v $(pwd)/kdesrc-buildrc:/home/developer/.kdesrc-buildrc -v $(pwd)/bashrc:/home/developer/.bashrc fedora-kdedev -c /bin/bash
docker run --rm -ti --privileged -v $WORKDIR:/work -v $(pwd)/kdesrc-buildrc:/home/developer/.kdesrc-buildrc -v $(pwd)/bashrc:/home/developer/.bashrc fedora-kdedev -c /home/developer/kdesrc-build/kdesrc-build
