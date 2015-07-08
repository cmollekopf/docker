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
    docker["build", "-t", tmpname, SCRIPT_DIR+"/kolab/"] & FG
    print("Starting tmpcontainer...")
    container = docker["run", "-d",
            "-h", settings.HOSTNAME,
            "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
            "-v", SCRIPT_DIR+"/kolab/fixRoundcubeT243.sh:/usr/share/roundcubemail/fixRoundcubeT243.sh",
            "-v", SCRIPT_DIR+"/kolab/fixRoundcubeT615.patch:/fixRoundcubeT615.patch",
            tmpname]().rstrip()

    print("Setting up kolab")
    docker["exec", container,  "setup-kolab", "--default", "--timezone="+settings.TIMEZONE, "--directory-manager-pwd="+settings.LDAPPW, "--mysqlserver=new"] & FG

    print("Fixing roundcube")
    docker["exec", container, "bash", "/usr/share/roundcubemail/fixRoundcubeT243.sh"] & FG
    docker["exec", container, "patch", "-n", "/usr/share/roundcubemail/plugins/libcalendaring/libvcalendar.php", "/fixRoundcubeT615.patch"] & FG
    docker["exec", container, "systemctl", "restart", "httpd"] & FG

    print("Comitting results...")
    docker["commit", container, settings.kolabimagename("base")] & FG
    docker["stop", container] & FG
    docker["rm", container] & FG
