#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import settings
import dockerutils
import argparse

def process_output(line):
    print(line)

def srcbuild(options):
    main(options.command, options.env, options.args)

def setupSubparser(parser):
    parser.add_argument("env", help = "environment to use")
    parser.add_argument("command", help = "command to use (should be another subparser)")
    parser.add_argument('args', nargs=argparse.REMAINDER)
    parser.set_defaults(func=srcbuild)

def main(command, environment, commandargs):
    runargs = ( "-ti",
        "--rm",
        "--privileged",
        "-v", "~/kdebuild/{}:/work".format(environment),
        "-v", "{}/{}/{}/kdesrc-buildrc:/home/developer/.kdesrc-buildrc".format(settings.SCRIPT_DIR, "kdesrcbuild", environment),
        "-v", "{}/{}/bashrc:/home/developer/.bashrc".format(settings.SCRIPT_DIR, "kdesrcbuild"),
    )
    image="fedora-kdedev"

    if command == "shell":
        subprocess.call("docker run {defaultargs} {image} -c bash".format(defaultargs=" ".join(runargs), image=image), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
    if command == "make":
        project = commandargs[0]
        print("Installing {}".format(project))
        args = ("-w", "/work/build/{project}".format(project=project))
        command = 'make'
        subprocess.call("docker run {defaultargs} {args} {image} -c '{command}'".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
    if command == "install":
        project = commandargs[0]
        print("Installing {}".format(project))
        args = ("-w", "/work/build/{project}".format(project=project))
        command = 'make install'
        subprocess.call("docker run {defaultargs} {args} {image} -c '{command}'".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
    if command == "kdesrcbuild":
        args = ()
        #Create the root dir so it is created with the correct rights
        subprocess.call("mkdir ~/kdebuild/{}".format(environment), shell=True)
        command = '/home/developer/kdesrc-build/kdesrc-build'
        if commandargs:
            command += ' ' + ' '.join(commandargs);
        subprocess.call("docker run {defaultargs} {args} {image} -c '{command}'".format(defaultargs=" ".join(runargs), args=" ".join(args), image=image, command=command), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
