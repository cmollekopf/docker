#!/usr/bin/env python2
from sh import docker
import settings
import sys

from . import BASEPATH

def srcbuild(options):
    for buildenvironment in options.buildenvironment:
        main(buildenvironment)

def setupSubparser(parser):
    parser.add_argument("buildenvironment", choices=["fedora-kde", "debian-kde", "debian-kf5", "fedora-libkolabkf5"], nargs="+", help = "buildenvironment to build")
    parser.set_defaults(func=srcbuild)

def main(buildenvironment):
    docker.build("-t", "{buildenvironment}dev".format(buildenvironment=buildenvironment), "{}/buildenvironments/{buildenvironment}/".format(BASEPATH, buildenvironment=buildenvironment), _out=sys.stdout)
