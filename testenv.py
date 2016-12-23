#!/usr/bin/env python2
import sh
import subprocess
import sys
import argparse

import kolab
import kolabpopulated
import kontact
import kdesrcbuild
import pep
import kube
import kubestandalone
import packagetest
import release

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

def buildClient(options):
    kontact.build.main(options.dataset)

def buildKube(options):
    kube.build.main()

def buildKubestandalone(options):
    kubestandalone.build.main()

def buildPep(options):
    pep.build.main()

def buildRelease(options):
    release.build.main()

def buildServer(options):
    if options.dataset is None:
        Exception("needs a dataset to build")
    buildImage(settings.REPOSITORY, "base", settings.REBUILD, lambda: kolab.build.main())
    buildImage(settings.REPOSITORY, settings.populatedTag(options.dataset), settings.REBUILD, lambda: kolabpopulated.build.main(options.dataset))

def buildKdesrcbuild(options):
    kdesrcbuild.build.srcbuild(options)

def start(options):
    dataset = options.dataset
    clientconfigset = options.clientconfigset
    standalone = clientconfigset is None
    if standalone:
        print("start " + dataset + " in background")
    else:
        print("start " + dataset + " " + clientconfigset)

    container = None
    started = False
    if dataset:
        cname = "{}:{}".format(settings.REPOSITORY, settings.populatedTag(dataset))
        started = dockerutils.findContainer(cname) == ""
        container = startContainer(cname, lambda: kolabpopulated.run.main(dataset, standalone))
    if clientconfigset == "pep":
        pep.run.main()
    elif clientconfigset == "kube":
        kube.run.main(container)
    elif clientconfigset == "release":
        release.run.main()
    elif clientconfigset == "kubestandalone":
        kubestandalone.run.main()
    elif not standalone:
        kontact.run.main(container, clientconfigset)
        if started:
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
    parser_build.add_argument("--rebuild", action='store_true', help = "rebuild the container")

    buildsubparsers = parser_build.add_subparsers(help='build variants')

    parser_build_server = buildsubparsers.add_parser('server', help = "build server")
    parser_build_server.add_argument("dataset", choices=["set1"], nargs="?", default="set1", help = "dataset to use")
    parser_build_server.set_defaults(func=buildServer)

    parser_build_kube = buildsubparsers.add_parser('kube', help = "build kube test env")
    parser_build_kube.set_defaults(func=buildKube)

    parser_build_kube = buildsubparsers.add_parser('kubestandalone', help = "build kube test env")
    parser_build_kube.set_defaults(func=buildKubestandalone)

    parser_build_pep = buildsubparsers.add_parser('pep', help = "build pep test env")
    parser_build_pep.set_defaults(func=buildPep)

    parser_build_pep = buildsubparsers.add_parser('release', help = "build release docker")
    parser_build_pep.set_defaults(func=buildRelease)

    parser_build_client = buildsubparsers.add_parser('client', help = "build client")
    parser_build_client.add_argument("dataset", choices=["john", "jane"], help = "dataset to use")
    parser_build_client.set_defaults(func=buildClient)

    parser_build_srcbuild = buildsubparsers.add_parser('kdesrcbuild', help = "create a sourcebuild")
    kdesrcbuild.build.setupSubparser(parser_build_srcbuild)
    parser_build_srcbuild.set_defaults(func=buildKdesrcbuild)

    parser_build_packagetest = buildsubparsers.add_parser('packagetest', help = "create images for test package installations")
    packagetest.build.setupSubparser(parser_build_packagetest)
    parser_build_packagetest.set_defaults(func=packagetest.build.srcbuild)

    parser.add_argument("--distro", default="fedora", help = "distro to build")
    parser.add_argument("--env", default="kde",  help = "environment to build")

    parser_start = subparsers.add_parser('start', help = "start a docker environment")
    parser_start.add_argument("dataset", choices=["set1", ""], help = "server dataset to use")
    parser_start.add_argument("clientconfigset", choices=["john", "jane", "pep", "kube", "kubestandalone", "release"], nargs="?", default=None, help = "clientconfigset to use")
    parser_start.set_defaults(func=start)

    parser_shell = subparsers.add_parser('shell', help = "get a shell in a running docker environment")
    parser_shell.add_argument("dataset", choices=["set1"], default="set1", help = "dataset of container (this should rather be a name or so)")
    parser_shell.set_defaults(func=shell)

    parser_srcbuild = subparsers.add_parser('srcbuild', help = "do a sourcebuild")
    kdesrcbuild.run.setupSubparser(parser_srcbuild)

    parser_packagetest = subparsers.add_parser('packagetest', help = "do test package installations")
    packagetest.run.setupSubparser(parser_packagetest)
    parser_packagetest.set_defaults(func=packagetest.run.run)

    options = parser.parse_args()
    if "rebuild" in vars(options):
        settings.REBUILD = options.rebuild

    options.func(options)

if __name__ == "__main__":
    main()
