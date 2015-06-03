#!/usr/bin/env python2
from sh import docker
import subprocess
import os
import sys

from settings import config

def process_output(line):
    print(line)

def main(dataset):
    containername="kontact"

    fdict = {"c": config,
            "dataset": dataset,
            "containername": containername}

    print("Building kontact...")
    docker.build("-t", containername, "{c.SCRIPT_DIR}/kontact/.".format(**fdict))

    print("Building {dataset}'s kontact...".format(**fdict))
    docker.build("-t", "{containername}:{dataset}".format(**fdict), "-f", "{c.SCRIPT_DIR}/kontact/Dockerfile-{dataset}".format(**fdict), "{c.SCRIPT_DIR}/kontact/.".format(**fdict))
