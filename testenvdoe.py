#!/usr/bin/env python2
import sh
import subprocess

def findContainer(name):
    container=""
    try:
        container = sh.awk("{print $1}", _in=sh.head("-n 1", _in=sh.grep(name, _in=sh.docker("ps", "-a"))))
    except:
        print "container not available"
    return container.rstrip()

containerName="kolab/kolabtestcontainer:latest"
container=findContainer(containerName)

if not container:
    print "starting container"
    subprocess.call("./run.sh", shell=True, cwd="kolab")
    container=findContainer(containerName)

print container
subprocess.call("./run.sh", shell=True, cwd="kontact")
sh.docker("stop", container)
sh.docker("rm", container)
