#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os
import sys

from settings import config
import settings

def main():
    containername="release"
    dataset="default"

    fdict = {"c": config,
            "containername": containername}

    print("Building release docker...")
    docker.build("-t", containername, "{c.SCRIPT_DIR}/release/.".format(**fdict), _out=sys.stdout)
