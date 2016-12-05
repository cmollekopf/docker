#!/usr/bin/env python2
from sh import docker
import settings
import os, sys

from . import BASEPATH

def srcbuild(options):
    for buildenvironment in options.buildenvironment:
        main(buildenvironment)

def setupSubparser(parser):
    choises =  [i for i in os.listdir(BASEPATH) if os.path.isdir(os.path.join(BASEPATH,i))]
    parser.add_argument("buildenvironment", choices=choises, nargs="+", help = "buildenvironment to build")
    parser.set_defaults(func=srcbuild)

def main(buildenvironment):
    containername="packagetest:{buildenvironment}".format(buildenvironment=buildenvironment)
    docker.build(settings.dockerCacheString(), "-t", containername, "{}/{buildenvironment}".format(BASEPATH, buildenvironment=buildenvironment), _out=sys.stdout)
