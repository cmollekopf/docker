#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import settings
import dockerutils
import argparse
import os
import re
from x11support import X11Support
import dockerutils
import kolabpopulated
from testenv import startContainer

from . import BASEPATH

def run(options):
    main(options.distro, options.args, options)

def setupSubparser(parser):
    choises =  [i for i in os.listdir(BASEPATH) if os.path.isdir(os.path.join(BASEPATH,i))]
    parser.add_argument("--no-x11forward", action='store_true', help = "forward x11 to docker", default=False)
    parser.add_argument("--xvfb", action='store_true', help = "start xvfb with start", default=False)
    parser.add_argument("distro", choices=choises, help = "distro/environment to use")
    parser.add_argument('args', nargs=argparse.REMAINDER)
    parser.set_defaults(func=run)

def main(environment, commandargs, options):

    dataset = "populated-set1"
    standalone = False
    cname = "{}:{}".format(settings.REPOSITORY, dataset)
    started = dockerutils.findContainer(cname) == ""
    kolabcontainer = startContainer(cname, lambda: kolabpopulated.run.main(dataset, standalone))

    runargs = [ "-ti",
        "--rm",
        "--privileged",
        "-v", "{}/{}/bashrc:/home/developer/.bashrc".format(BASEPATH, environment),
        "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
        "-e", "START_XVFB={}".format(str(options.xvfb).lower()),
        "--link", "{}:kolab".format(kolabcontainer),
        ]

    if not options.no_x11forward:
        x11 = X11Support()
        x11.setupX11Authorization()
        runargs.extend(x11.docker_args())

    # Mount all files from the environment into the container
    path = "{}/{}".format(BASEPATH, environment)
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fn in filenames:
            if fn in ("Dockerfile", "bashrc"):
                continue
            runargs.extend(["-v", "{}:/home/developer/{}".format(os.path.join(dirpath,fn), fn)])

    image="packagetest:{}".format(environment)

    runargs.append(image)
    runargs.extend(["-t", "-c","bash"])
    args = ["docker","run"]
    args.extend(runargs)
    subprocess.call(" ".join(args), shell=True, cwd=settings.SCRIPT_DIR)
