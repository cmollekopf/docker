#!/usr/bin/env python2
import sh
import subprocess
import sys
import kolab
from kolab import build
import kolabpopulated
from kolabpopulated import build
from kolabpopulated import run
import kontact
from kontact import build
from kontact import run
import kdesrcbuild
from kdesrcbuild import run

import settings
import dockerutils

def buildImage(repo, tag, rebuild, builder):
    image = dockerutils.findImage(repo, tag)
    if not image or rebuild:
        print("building image: " + repo + ":" + tag)
        builder()
        image = dockerutils.findImage(repo, tag)
    print("Image is ready: {}:{} {}".format(repo, tag, image))
    return image

def startContainer(name, runner):
    container=dockerutils.findContainer(name)
    if not container:
        runner()
        container = dockerutils.findContainer(name)
    print("Container is ready: {} {}".format(name, container))
    return container

def main(command, argv):
    if command == "build":
        target = argv[2]
        if target == "server":
            dataset = argv[3]
            buildImage(settings.REPOSITORY, "base", False, lambda: kolab.build.main)
            buildImage(settings.REPOSITORY, settings.populatedTag(dataset), True, lambda: kolabpopulated.build.main(dataset))
        if target == "client":
            # buildImage("kontact", "john", False, lambda: kontact.build.main("john"))
            kontact.build.main("john")
            kontact.build.main("jane")
    if command == "start":
        print("start")
        dataset = argv[2]
        clientconfigset = argv[3]
        container = startContainer("{}:{}".format(settings.REPOSITORY, settings.populatedTag(dataset)), lambda: kolabpopulated.run.main(dataset))
        kontact.run.main(container, clientconfigset)
        sh.docker.kill(container)
        sh.docker.rm(container)
    if command == "shell":
        dataset = "set1"
        container = dockerutils.findContainer("{}:{}".format(settings.REPOSITORY, settings.populatedTag(dataset)))
        subprocess.call("docker exec -i -t {} bash".format(container), shell=True)
    if command == "srcbuild":
        command = argv[2]
        project = argv[3]
        kdesrcbuild.run.main(command, project)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv)

# * build $env
# ** build server with defined dataset
# ** build client(s)

# * start $env
# ** start server
# ** start client(s) with link to server



