#!/usr/bin/env python2
import sh
import subprocess

subprocess.call("docker run --rm -ti --privileged -v ~/kdebuild/fedora:/work -v $(pwd)/kdesrc-buildrc:/home/developer/.kdesrc-buildrc -v $(pwd)/bashrc:/home/developer/.bashrc fedora-kdedev -c /home/developer/kdesrc-build/kdesrc-build", shell=True, cwd=".")
