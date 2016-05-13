#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os
import sys

from settings import config
import settings

def main():
    containername="kube"
    dataset="default"

    fdict = {"c": config,
            "dataset": dataset,
            "containername": containername}

    print("Building kube...")
    docker.build(settings.dockerCacheString(), "-t", containername, "{c.SCRIPT_DIR}/kube/.".format(**fdict), _out=sys.stdout)

    print("Building {dataset}'s kube...".format(**fdict))
    docker.build(settings.dockerCacheString(), "-t", "{containername}:{dataset}".format(**fdict), "-f", "{c.SCRIPT_DIR}/kube/Dockerfile-{dataset}".format(**fdict), "{c.SCRIPT_DIR}/kube/.".format(**fdict), _out=sys.stdout)
