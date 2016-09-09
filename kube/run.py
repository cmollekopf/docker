#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os

import settings
import dockerutils
from x11support import X11Support

from . import BASEPATH

def main(kolabcontainer):
    containername="kube"
    configset="default"

    runargs = [
        "--rm",
        "-ti",
        "--privileged",
        "-u", "developer",
        "--security-opt", "seccomp:unconfined", # Necessary to get gdb to work
        "--device", "/dev/dri/card0:/dev/dri/card0",
        "--device", "/dev/dri/renderD128:/dev/dri/renderD128",
        "--device", "/dev/dri/controlD64:/dev/dri/controlD64",
        "-v", "{}/kube:/work".format(settings.ROOT),
        "-v", "{}/testmails:/home/developer/maildir1/testmails".format(BASEPATH),
    ]
    if kolabcontainer:
        runargs.extend([
            "--link", "{}:kolab".format(kolabcontainer),
        ]);

    x11 = X11Support()
    x11.setupX11Authorization()
    runargs.extend(x11.docker_args())
    runargs.extend([
        "{}:{}".format(containername, configset),
        "/bin/bash"
    ]);

    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    subprocess.call("docker run " + " ".join(runargs), shell=True)
