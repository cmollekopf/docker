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

import settings
import dockerutils

def buildImage(repo, tag, rebuild, builder):
    image = dockerutils.findImage(repo, tag)
    if not image or rebuild:
        print("building image: " + repo + ":" + tag)
        builder()
        image = dockerutils.findImage(repo, tag)
    print("Image is ready: {}:{}".format(repo, tag))
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
            baseimage = buildImage(settings.REPOSITORY, "base", False, lambda: kolab.build.main)
            populatedbuild = buildImage(settings.REPOSITORY, settings.populatedTag(dataset), False, lambda: kolabpopulated.build.main(dataset))
        if target == "client":
            buildImage("kontact", "latest", False, lambda: kontact.build.main)
    if command == "start":
        print("start")
        dataset = argv[2]
        container = startContainer("{}:{}".format(settings.REPOSITORY, settings.populatedTag(dataset)), lambda: kolabpopulated.run.main(dataset))
        kontact.run.main(container)
        sh.docker.kill(container)
        sh.docker.rm(container)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv)

# * build $env
# ** build server with defined dataset
# ** build client(s)

# * start $env
# ** start server
# ** start client(s) with link to server



