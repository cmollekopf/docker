#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os
import sys

import settings
import dockerutils

def process_output(line):
    print(line)

def setupX11Authorization(xauthFile, display):
    try:
        sh.touch(xauthFile)
    except:
        print("touch failed")
    sh.xauth(sh.sed(sh.xauth("nlist", display), "-e", 's/^..../ffff/'), "-f", xauthFile, "nmerge", "-")

def main(kolabcontainer):
    containername="kontact"

    SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
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
        "--device=/dev/dri/card0:/dev/dri/card0",
        "-v", "{}:{}".format(XAUTH, XAUTH),
        "-v", "/tmp/.X11-unix:/tmp/.X11-unix",
        "-v", "{}:/opt/kde".format(settings.KDEROOT),
        "kontact:latest",
        "/bin/bash"
    )
    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    subprocess.call("docker run " + " ".join(runargs), shell=True)
