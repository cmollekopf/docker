#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os

import settings
import dockerutils

def setupX11Authorization(xauthFile, display):
    try:
        sh.touch(xauthFile)
    except:
        print("touch failed")
    sh.xauth(sh.sed(sh.xauth("nlist", display), "-e", 's/^..../ffff/'), "-f", xauthFile, "nmerge", "-")

def main(kolabcontainer, configset):
    containername="kontact"

    DISPLAY = os.environ.get('DISPLAY')
    XAUTH="/tmp/.docker.xauth"
    setupX11Authorization(XAUTH, DISPLAY)

    runargs = (
        "--rm",
        "-ti",
        "-u", "developer",
        "--link", "{}:kolab".format(kolabcontainer),
        "-e", "DISPLAY={}".format(DISPLAY),
        "-e", "XAUTHORITY={}".format(XAUTH),
        "--device", "/dev/dri/card0:/dev/dri/card0",
        "--device", "/dev/dri/renderD128:/dev/dri/renderD128",
        "--device", "/dev/dri/controlD64:/dev/dri/controlD64",
        "-v", "{}:{}".format(XAUTH, XAUTH),
        "-v", "/tmp/.X11-unix:/tmp/.X11-unix",
        "-v", "{}:/opt/kde".format(settings.KDEROOT),
        "{}:{}".format(containername, configset),
        "/bin/bash"
    )
    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    subprocess.call("docker run " + " ".join(runargs), shell=True)
