#!/usr/bin/env python2
from sh import docker
import subprocess
import time
import os
import sys

import settings

def process_output(line):
    print(line)

def main():
    tmpname = settings.kolabimagename("tmpbase")

    SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    print("Building tmpcontainer...")
    docker.build("--no-cache=true", "-t", tmpname, SCRIPT_DIR+"/kolab/", _out=process_output)
    print("Starting tmpcontainer...")
    print(SCRIPT_DIR+"/fixRoundcubeT243.sh:/usr/share/roundcubemail/fixRoundcubeT243.sh")
    container = docker.run("-d", "-h", settings.HOSTNAME, "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro", "-v", SCRIPT_DIR+"/kolab/fixRoundcubeT243.sh:/usr/share/roundcubemail/fixRoundcubeT243.sh", tmpname).rstrip()

    print("Setting up kolab")
    docker("exec", container,  "setup-kolab", "--default", "--timezone="+settings.TIMEZONE, "--directory-manager-pwd="+settings.LDAPPW, "--mysqlserver=new", _out=process_output)

    print("Fixing roundcube")
    docker("exec", container, "bash", "/usr/share/roundcubemail/fixRoundcubeT243.sh", _out=process_output)
    docker("exec", container, "systemctl", "restart", "httpd", _out=process_output)

    print("Comitting results...")
    docker.commit(container, settings.kolabimagename("base"))
    docker.stop(container)
    docker.rm(container)
