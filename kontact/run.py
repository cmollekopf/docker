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

def setupConfigDirs(dirname, fullPrimaryEmail, primaryEmail, name, uid):
    basedir = settings.SCRIPT_DIR + "/kontact"
    print(basedir);
    try:
        sh.rm("-R", )
    except:
        print("nothing to remove")
    sh.cp("-R", "{}/config".format(basedir), "{}/{}".format(basedir, dirname))
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{fullPrimaryEmail}/" + fullPrimaryEmail + "/g", "{}", "+")
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{primaryEmail}/" +  primaryEmail + "/g", "{}", "+")
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{name}/" + name + "/g", "{}", "+")
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{uid}/" + uid + "/g", "{}", "+")

def main(kolabcontainer, configset):
    containername="kontact"

    DISPLAY = os.environ.get('DISPLAY')
    XAUTH="/tmp/.docker.xauth"
    setupX11Authorization(XAUTH, DISPLAY)
    setupConfigDirs("john", "john.doe@example.org", "doe@example.org", "John Doe", "doe")
    setupConfigDirs("jane", "jane.doe@example.org", "doe2@example.org", "Jane Doe", "doe2")

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
        "{}:{}".format(containername, configset),
        "/bin/bash"
    )
    # docker.run(*runargs, _out=process_output, _tty_out=True, _tty_in=True)
    # subprocess.call("docker run " + " ".join(runargs), shell=True)
