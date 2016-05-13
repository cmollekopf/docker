#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os
import sys

from settings import config
import settings

def setupConfigDirs(dirname, fullPrimaryEmail, primaryEmail, name, uid):
    basedir = settings.SCRIPT_DIR + "/kontact"
    print(basedir);
    try:
        sh.rm("-R", )
    except:
        print("nothing to remove")
    sh.cp("-R", "{}/config".format(basedir), "{}/{}".format(basedir, dirname))
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{fullPrimaryEmail}/" + fullPrimaryEmail + "/g", "{}", "+")
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{primaryEmail}/" +  primaryEmail + "/g", "{}", "+")
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{name}/" + name + "/g", "{}", "+")
    sh.find("{}/{}".format(basedir, dirname), "-type", "f", "-exec", "sed", "-i", "s/{uid}/" + uid + "/g", "{}", "+")

def main(dataset):
    containername="kontact"

    if dataset == "john":
        setupConfigDirs("john", "john.doe@example.org", "doe@example.org", "John Doe", "doe")
    if dataset == "jane":
        setupConfigDirs("jane", "jane.doe@example.org", "doe2@example.org", "Jane Doe", "doe2")

    fdict = {"c": config,
            "dataset": dataset,
            "containername": containername}

    print("Building kontact...")
    docker.build(settings.dockerCacheString(), "-t", containername, "{c.SCRIPT_DIR}/kontact/.".format(**fdict), _out=sys.stdout)

    print("Building {dataset}'s kontact...".format(**fdict))
    docker.build(settings.dockerCacheString(), "-t", "{containername}:{dataset}".format(**fdict), "-f", "{c.SCRIPT_DIR}/kontact/Dockerfile-{dataset}".format(**fdict), "{c.SCRIPT_DIR}/kontact/.".format(**fdict), _out=sys.stdout)
