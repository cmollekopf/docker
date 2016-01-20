#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os

import settings
import dockerutils
from x11support import X11Support

def main():
    containername="kubestandalone"
    configset="default"

    runargs = [
        "--rm",
        "-ti",
        "-u", "developer",
        "--device", "/dev/dri/card0:/dev/dri/card0",
        "--device", "/dev/dri/renderD128:/dev/dri/renderD128",
        "--device", "/dev/dri/controlD64:/dev/dri/controlD64",
        # "-v", "{}/akonadinext:/work".format(settings.ROOT),
    ]

    x11 = X11Support()
    x11.setupX11Authorization()
    runargs.extend(x11.docker_args())
    runargs.extend([
        "{}:{}".format(containername, configset),
        "/bin/bash"
    ]);

    print("docker run " + " ".join(runargs))
    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    subprocess.call("docker run " + " ".join(runargs), shell=True)
