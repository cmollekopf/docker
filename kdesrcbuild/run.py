#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import settings

def process_output(line):
    print(line)

def main(command, project):
    if command == "shell":
        subprocess.call("docker run --rm -ti --privileged -v ~/kdebuild/fedora:/work -v $(pwd)/kdesrc-buildrc:/home/developer/.kdesrc-buildrc -v $(pwd)/bashrc:/home/developer/.bashrc fedora-kdedev -c bash", shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
    if command == "install":
        print("Installing {}".format(project))
        runargs = (
            "--rm",
            # "-ti",
            "--privileged",
            "-v",
            "/home/chrigi/kdebuild/fedora:/work",
            "-v", "{}/{}/kdesrc-buildrc:/home/developer/.kdesrc-buildrc".format(settings.SCRIPT_DIR, "kdesrcbuild"),
            "-v", "{}/{}/bashrc:/home/developer/.bashrc".format(settings.SCRIPT_DIR, "kdesrcbuild"),
            "-w", "/work/build/{project}".format(project=project),
            "fedora-kdedev",
            "-c pwd && make install"
        )
        # docker.run(*runargs, _out=process_output);
        subprocess.call("docker run " + " ".join(runargs), shell=True, cwd=settings.SCRIPT_DIR+"/kdesrcbuild")
# docker run --rm -ti --privileged -v $WORKDIR:/work -v $(pwd)/kdesrc-buildrc:/home/developer/.kdesrc-buildrc -v $(pwd)/bashrc:/home/developer/.bashrc fedora-kdedev -c /bin/bash
