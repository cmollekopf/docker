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

    print("Building kontact...")
    docker.build("-t", containername, "{}/kontact/.".format(settings.SCRIPT_DIR))

    print("Building {}'s kontact...".format(dataset))
    docker.build("-t", "{}:{}".format(containername, dataset), "-f", "{}/kontact/Dockerfile-{}".format(settings.SCRIPT_DIR, dataset), "{}/kontact/.".format(settings.SCRIPT_DIR))
