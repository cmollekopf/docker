#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os

import settings
import dockerutils
from x11support import X11Support

def main(kolabcontainer, configset):
    containername="kontact"

    runargs = [
        "--rm",
        "-ti",
        "-u", "developer",
        "--security-opt", "seccomp:unconfined", # Necessary to get gdb to work
        "--link", "{}:kolab".format(kolabcontainer),
        "--device", "/dev/dri/card0:/dev/dri/card0",
        "--device", "/dev/dri/renderD128:/dev/dri/renderD128",
        "--device", "/dev/dri/controlD64:/dev/dri/controlD64",
        "-v", "{}:/opt/kde".format(settings.KDEROOT),
    ]

    x11 = X11Support()
    x11.setupX11Authorization()
    runargs.extend(x11.docker_args())
    runargs.extend([
        "{}:{}".format(containername, configset),
        "/bin/bash"
    ]);

    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    subprocess.call("docker run " + " ".join(runargs), shell=True)
