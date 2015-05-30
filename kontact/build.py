#!/usr/bin/env python2
from sh import docker
import subprocess
import os
import sys

import settings

def process_output(line):
    print(line)

def main(dataset):
    containername="kontact"

    SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    print("Building kontact...")
    docker("build", "-t", containername, SCRIPT_DIR+"/kontact/.")
