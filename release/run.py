#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os

import settings
import dockerutils
from x11support import X11Support

from . import BASEPATH

def main():
    containername="release"

    runargs = [
        "--rm",
        "-ti",
        "-u", "developer",
        "-v", "{}/kdepim:/work".format(settings.ROOT),
        "-v", "{}/bashrc:/home/developer/.bashrc".format(BASEPATH),
        "-v", "{}/setuprepos.sh:/home/developer/setuprepos.sh".format(BASEPATH),
        "-v", "{}/release:/home/developer/release".format(BASEPATH),
        "-v", "~/.oscrc:/home/developer/.oscrc",
        "-v", "{}/config.cfg:/home/developer/.docker.cfg".format(settings.SCRIPT_DIR),
    ]
    runargs.extend([
        "{}".format(containername),
    ]);

    subprocess.call("docker run " + " ".join(runargs), shell=True)
