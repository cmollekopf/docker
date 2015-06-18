#!/usr/bin/env python2
import sh
import subprocess
import sys
import argparse
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

def build(options):
    print("build " + options.dataset + options.target)
    if options.target == "server":
        buildImage(settings.REPOSITORY, "base", False, lambda: kolab.build.main())
        buildImage(settings.REPOSITORY, settings.populatedTag(options.dataset), True, lambda: kolabpopulated.build.main(options.dataset))
    if options.target == "client":
        # buildImage("kontact", "john", False, lambda: kontact.build.main("john"))
        kontact.build.main("john")
        kontact.build.main("jane")

def start(options):
    print("start " + options.dataset + options.clientconfigset)
    dataset = options.dataset
    clientconfigset = options.clientconfigset
    container = startContainer("{}:{}".format(settings.REPOSITORY, settings.populatedTag(dataset)), lambda: kolabpopulated.run.main(dataset))
    kontact.run.main(container, clientconfigset)
    sh.docker.kill(container)
    sh.docker.rm(container)

def shell(options):
    print "shell " + options.dataset
    container = dockerutils.findContainer("{}:{}".format(settings.REPOSITORY, settings.populatedTag(options.dataset)))
    subprocess.call("docker exec -i -t {} bash".format(container), shell=True)

def srcbuild(options):
    print "srcbuild " + options.command + options.project
    kdesrcbuild.run.main(options.command, options.project)

def main():
    usage = "usage: %prog [options]"
    parser = argparse.ArgumentParser(usage)
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_build = subparsers.add_parser('build', help = "build a docker image")
    parser_build.add_argument("target", choices=["server", "client"], help = "image to build")
    parser_build.add_argument("dataset", choices=["set1"], help = "dataset to use")
    parser_build.set_defaults(func=build)

    parser_start = subparsers.add_parser('start', help = "start a docker environment")
    parser_start.add_argument("dataset", choices=["set1"], help = "server dataset to use")
    parser_start.add_argument("clientconfigset", choices=["john", "jane"], help = "clientconfigset to use")
    parser_start.set_defaults(func=start)

    parser_shell = subparsers.add_parser('shell', help = "get a shell in a running docker environment")
    parser_shell.add_argument("dataset", choices=["set1"], default="set1", help = "dataset of container (this should rather be a name or so)")
    parser_shell.set_defaults(func=shell)

    parser_srcbuild = subparsers.add_parser('srcbuild', help = "do a sourcebuild")
    parser_srcbuild.add_argument("command", help = "command to use (should be another subparser)")
    parser_srcbuild.add_argument("project", help = "project to build")
    parser_srcbuild.set_defaults(func=srcbuild)

    options = parser.parse_args()
    options.func(options)

if __name__ == "__main__":
    main()
