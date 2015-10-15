#!/usr/bin/env python2
import sh
import subprocess
import sys
import argparse

import kolab
import kolabpopulated
import kontact
import kdesrcbuild

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
    container = dockerutils.findContainer(name)
    if not container:
        runner()
        container = dockerutils.findContainer(name)
    print("Container is ready: {} {}".format(name, container))
    return container

def build(options):
    if (options.target == "server" or options.target == "all") and options.dataset is None:
        Exception("needs a dataset to build")
    else:
        print("build " + options.target)
    if options.target == "server":
        print("build " + options.dataset + " " + options.target)
        buildImage(settings.REPOSITORY, "base", False, lambda: kolab.build.main())
        buildImage(settings.REPOSITORY, settings.populatedTag(options.dataset), True, lambda: kolabpopulated.build.main(options.dataset))
    if options.target == "client" or options.target == "all":
        # buildImage("kontact", "john", False, lambda: kontact.build.main("john"))
        kontact.build.main("john")
        kontact.build.main("jane")
    if options.target == "kdesrcbuild" or options.target == "all":
        kdesrcbuild.build.srcbuild(options)

def start(options):
    dataset = options.dataset
    clientconfigset = options.clientconfigset
    standalone = clientconfigset is None
    if standalone:
        print("start " + dataset + " in background")
    else:
        print("start " + dataset + " " + clientconfigset)

    cname = "{}:{}".format(settings.REPOSITORY, settings.populatedTag(dataset))
    started = dockerutils.findContainer(cname) != ""
    container = startContainer(cname, lambda: kolabpopulated.run.main(dataset, standalone))
    if not standalone:
        kontact.run.main(container, clientconfigset)
        if not started:
            sh.docker.kill(container)
            sh.docker.rm(container)

def shell(options):
    print "shell " + options.dataset
    container = dockerutils.findContainer("{}:{}".format(settings.REPOSITORY, settings.populatedTag(options.dataset)))
    subprocess.call("docker exec -i -t {} bash".format(container), shell=True)

def main():
    usage = "usage: %prog [options]"
    parser = argparse.ArgumentParser(usage)
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_build = subparsers.add_parser('build', help = "build a docker image")

    buildsubparsers = parser_build.add_subparsers(help='build variants')
    parser_all = buildsubparsers.add_parser('server', help = "build server")
    parser_all.add_argument("dataset", choices=["set1"], nargs="?", default="set1", help = "dataset to use")
    parser_all.set_defaults(func=build)

    parser_all = buildsubparsers.add_parser('client', help = "build client")
    parser_all.set_defaults(func=build)

    parser_srcbuild = buildsubparsers.add_parser('kdesrcbuild', help = "create a sourcebuild")
    kdesrcbuild.build.setupSubparser(parser_srcbuild)

    parser_all = buildsubparsers.add_parser('all', help = "build everything")
    parser_all.add_argument("dataset", choices=["set1"], nargs="?", default="set1", help = "dataset to use")
    parser.add_argument("--distro", default="fedora", help = "distro to build")
    parser.add_argument("--env", default="kde",  help = "environment to build")
    parser_all.set_defaults(func=build)

    parser_start = subparsers.add_parser('start', help = "start a docker environment")
    parser_start.add_argument("dataset", choices=["set1"], help = "server dataset to use")
    parser_start.add_argument("clientconfigset", choices=["john", "jane"], nargs="?", default=None, help = "clientconfigset to use")
    parser_start.set_defaults(func=start)

    parser_shell = subparsers.add_parser('shell', help = "get a shell in a running docker environment")
    parser_shell.add_argument("dataset", choices=["set1"], default="set1", help = "dataset of container (this should rather be a name or so)")
    parser_shell.set_defaults(func=shell)

    parser_srcbuild = subparsers.add_parser('srcbuild', help = "do a sourcebuild")
    kdesrcbuild.run.setupSubparser(parser_srcbuild)

    options = parser.parse_args()
    options.func(options)

if __name__ == "__main__":
    main()
