#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import settings
import dockerutils
import argparse
import os

BASEPATH = os.path.dirname(os.path.realpath(__file__))

def srcbuild(options):
    main(options.command, options.env, options.args, options)

def setupSubparser(parser):
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
        "-v", "{}/build-de.sh:/home/developer/build-de.sh".format(BASEPATH),
    ]
    image="{}-kdedev".format(options.distro)
    if (options.distro == "debian" and environment == "kf5"):
        image = "debian-kf5dev"
    translatePathsToHost = "sed 's/\/work\//~\/kdebuild\/{distro}{environment}\//g'".format(distro=distro, environment=environment)
    if command == "shell":
	runargs.append(image)
	runargs.extend(["-c","bash"])
	args = ["docker","run"]
	args.extend(runargs)
        subprocess.call(" ".join(args), shell=True, cwd=settings.SCRIPT_DIR)
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
        args = ("-w", "/work/build/{project}".format(project=project))
        command = " ".join(commandargs)
        subprocess.call("docker run {defaultargs} {args} {image} -c 'source /home/developer/.bashrc && {command}' | {translatePathsToHost}".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command, translatePathsToHost=translatePathsToHost), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")

if __name__ == "__main__":
	main("shell", "kdepim", ())
