#!/usr/bin/env python2
import subprocess
import time
import os
import sys
from plumbum.cmd import docker
from plumbum import FG

import settings

def main():
    tmpname = settings.kolabimagename("tmpbase")

    SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    print("Building tmpcontainer...")
    # docker["build", "--no-cache=true", "-t", tmpname, SCRIPT_DIR+"/kolab/"] & FG
    if settings.rebuild():
        docker["build", "--no-cache=true", "-t", tmpname, SCRIPT_DIR+"/kolab/"] & FG
    else:
        docker["build", "-t", tmpname, SCRIPT_DIR+"/kolab/"] & FG
    print("Starting tmpcontainer...")
    container = docker["run", "-d",
            "-h", settings.HOSTNAME,
            "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
            tmpname]().rstrip()

    print("Setting up kolab")
    docker["exec", container,  "setup-kolab", "--default", "--timezone="+settings.TIMEZONE, "--directory-manager-pwd="+settings.LDAPPW, "--mysqlserver=new"] & FG


    print("Comitting results...")
    docker["commit", container, settings.kolabimagename("base")] & FG
    docker["stop", container] & FG
    docker["rm", container] & FG
