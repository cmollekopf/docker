#!/usr/bin/env python2
from sh import docker
import subprocess
import time
import os
import sys

import settings

def process_output(line):
    print(line)

def main(dataset):
    tmpname="kolab/kolabtestcontainer:tmppopulated"
    imagename="kolab/kolabtestcontainer:populated-"+dataset

    SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    print("Building tmpcontainer...")
    docker.build("-t", tmpname, SCRIPT_DIR+"/kolabpopulated/.")
    print("Starting tmpcontainer...")
    container = docker.run("-d", "-h", settings.HOSTNAME, "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro", "-v", SCRIPT_DIR+"/kolabpopulated/"+dataset+"/:/data/", tmpname).rstrip()

    # Wait for imap to become available on imaps://localhost:993
    time.sleep(5)

    print("Running populate.sh...")
    docker("exec", container,  "/data/populate.sh", _out=process_output)

    print("Comitting results...")
    docker.commit(container, imagename)
    docker.stop(container)
    docker.rm(container)
