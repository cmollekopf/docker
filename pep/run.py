#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os

import settings
import dockerutils

def main():
    containername="pep"
    configset="default"

    runargs = (
        "--rm",
        "-ti",
        "-u", "developer",
        "-v", "{}/pep:/work".format(settings.ROOT),
        "{}:{}".format(containername, configset),
        "/bin/bash"
    )
    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    subprocess.call("docker run " + " ".join(runargs), shell=True)
