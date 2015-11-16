#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import settings
import dockerutils
import argparse
import os
from x11support import X11Support

from . import BASEPATH

def srcbuild(options):
    main(options.command, options.env, options.args, options)

def setupSubparser(parser):
    parser.add_argument("--icecream", action='store_true', help = "use icecream for compiling")
    parser.add_argument("--x11forward", action='store_true', help = "forward x11 to docker (needed for some tests)")
    parser.add_argument("--xvfb", action='store_true', help = "start xvfb with start")
    parser.add_argument("--distro", default="fedora", help = "distro to use")
    parser.add_argument("env", help = "environment to use")
    parser.add_argument("command", help = "command to use (should be another subparser). Is used for the project in case of arbitray command.")
    parser.add_argument('args', nargs=argparse.REMAINDER)
    parser.set_defaults(func=srcbuild)

def main(command, environment, commandargs, options):
    distro = ""
    if (options.distro != "fedora"):
        distro = "debian/"
    runargs = [ "-ti",
        "--rm",
        "--privileged",
        "-v", "~/kdebuild/{}{}:/work".format(distro, environment),
        "-v", "{}/{}/kdesrc-buildrc:/home/developer/.kdesrc-buildrc".format(BASEPATH, environment),
        "-v", "{}/bashrc:/home/developer/.bashrc".format(BASEPATH),
        "-v", "{}/start-iceccd.sh:/home/developer/.start-iceccd.sh".format(BASEPATH),
        "-e", "START_ICECREAM={}".format(str(options.icecream).lower()),
        "-e", "START_XVFB={}".format(str(options.xvfb).lower()),
        ]
    translatePathsToHost = "sed 's/\/work\//~\/kdebuild\/{distro}{environment}\//g'".format(distro=distro, environment=environment)

    if options.x11forward:
	    x11 = X11Support()
	    x11.setupX11Authorization()
	    runargs.extend(x11.docker_args())

    image="{}-kdedev".format(options.distro)
    if (options.distro == "debian" and environment == "kf5"):
        image = "debian-kf5dev"

    if command == "shell":
        runargs.append(image)
        runargs.extend(["-c","bash"])
        args = ["docker","run"]
        args.extend(runargs)
        subprocess.call(" ".join(args), shell=True, cwd=settings.SCRIPT_DIR)
    elif command == "build":
        args = ()
        #Create the root dir so it is created with the correct rights
        subprocess.call("mkdir -p ~/kdebuild/{}{}".format(distro, environment), shell=True)
        project = commandargs[0]
        runargs.extend(["-v", "{basepath}/{environment}/build-{project}.sh:/home/developer/build-{project}.sh".format(basepath=BASEPATH, environment=environment, project=project)])
        command = "/home/developer/build-{project}.sh".format(project=project)
        subprocess.call("docker run {defaultargs} {args} {image} -c 'source /home/developer/.bashrc && {command}' | {translatePathsToHost}".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command, translatePathsToHost=translatePathsToHost), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
    elif command == "kdesrcbuild":
        args = ()
        #Create the root dir so it is created with the correct rights
        subprocess.call("mkdir -p ~/kdebuild/{}{}".format(distro, environment), shell=True)
        command = '/home/developer/kdesrc-build/kdesrc-build'
        if commandargs:
            command += ' ' + ' '.join(commandargs);
        subprocess.call("docker run {defaultargs} {args} {image} -c 'source /home/developer/.bashrc && {command}' | {translatePathsToHost}".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command, translatePathsToHost=translatePathsToHost), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
    else:
        project = command
        print("Installing {}".format(project))
        if os.path.isabs(project):
            args = ("-w", "{project}".format(project=project))
        else:
            args = ("-w", "/work/build/{project}".format(project=project))
        command = " ".join(commandargs)
        subprocess.call("docker run {defaultargs} {args} {image} -c 'source /home/developer/.bashrc && {command}' | {translatePathsToHost}".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command, translatePathsToHost=translatePathsToHost), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")

if __name__ == "__main__":
	main("shell", "kdepim", ())
