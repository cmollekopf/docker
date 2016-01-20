#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os
import sys

from settings import config
import settings

def main():
    containername="kubestandalone"
    dataset="default"

    fdict = {"c": config,
            "dataset": dataset,
            "containername": containername}

    print("Building kubestandalone...")
    docker.build("-t", containername, "{c.SCRIPT_DIR}/kubestandalone/.".format(**fdict), _out=sys.stdout)

    print("Building kube...".format(**fdict))
    docker.build("-t", "{containername}:kdesrcbuild".format(**fdict), "-f", "{c.SCRIPT_DIR}/kubestandalone/Dockerfile-kdesrcbuild".format(**fdict), "{c.SCRIPT_DIR}/kubestandalone/.".format(**fdict), _out=sys.stdout)

    print("Building {dataset}'s kubestandalone...".format(**fdict))
    docker.build("-t", "{containername}:{dataset}".format(**fdict), "-f", "{c.SCRIPT_DIR}/kubestandalone/Dockerfile-{dataset}".format(**fdict), "{c.SCRIPT_DIR}/kubestandalone/.".format(**fdict), _out=sys.stdout)
