#!/usr/bin/env python2
from sh import docker
import settings
import sys

from . import BASEPATH

def srcbuild(options):
    main(options.distro, options.env)

def setupSubparser(parser):
    parser.add_argument("--distro", default="fedora", help = "distro to build")
    parser.add_argument("--env", default="kde",  help = "environment to build")
    parser.set_defaults(func=srcbuild)

def main(distro, env):
    docker.build("-t", "{distro}-{env}dev".format(distro=distro, env=env), "{}/{}/{}/".format(BASEPATH, distro, env), _out=sys.stdout)
