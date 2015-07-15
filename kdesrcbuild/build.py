#!/usr/bin/env python2
from sh import docker
import settings
import sys

def main():
    docker.build("-t", "fedora-kdedev", settings.SCRIPT_DIR+"/kdesrcbuild/", _out=sys.stdout)
