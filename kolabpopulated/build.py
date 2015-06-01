#!/usr/bin/env python2
from sh import docker
import subprocess
import time
import os
import sys

import settings

def process_output(line):
    print(line)

def generateUserFiles(template, outputfile, templateParams):
    with open(template) as f:
        data = f.read()

    with open(outputfile, "w") as f:
        data = data.format(**templateParams)
        f.write(data)

def main(dataset):
    tmpname="kolab/kolabtestcontainer:tmppopulated"
    imagename="kolab/kolabtestcontainer:populated-"+dataset
    basedir =  "{}/kolabpopulated".format(settings.SCRIPT_DIR)

    print("Building tmpcontainer...")
    docker.build("-t", tmpname, "{}/kolabpopulated/.".format(settings.SCRIPT_DIR))

    generateUserFiles("{}/user.ldif".format(basedir), "{}/set1/john.ldif".format(basedir), dict(
        name = "Doe",
        nameLower = "doe",
        givenName="John",
        givenNameLower="john",
        uid="doe",
        secondaryUid="j.doe",
        domain="example",
        domainExtension="org"
    ))

    generateUserFiles("{}/user.ldif".format(basedir), "{}/set1/jane.ldif".format(basedir), dict(
        name = "Doe",
        nameLower = "doe",
        givenName="Jane",
        givenNameLower="jane",
        uid="doe2",
        secondaryUid="j.doe2",
        domain="example",
        domainExtension="org"
    ))

    generateUserFiles("{}/user.ldif".format(basedir), "{}/set1/anna.ldif".format(basedir), dict(
        name = "Test",
        nameLower = "test",
        givenName="Anna",
        givenNameLower="anna",
        uid="test",
        secondaryUid="a.test",
        domain="example",
        domainExtension="org"
    ))

    generateUserFiles("{}/user.ldif".format(basedir), "{}/set1/rolf.ldif".format(basedir), dict(
        name = "Meier",
        nameLower = "meier",
        givenName="Rolf",
        givenNameLower="rolf",
        uid="meier",
        secondaryUid="r.meier",
        domain="example",
        domainExtension="org"
    ))

    generateUserFiles("{}/user.ldif".format(basedir), "{}/set1/franck.ldif".format(basedir), dict(
        name = "Bodum",
        nameLower = "bodum",
        givenName ="Franck",
        givenNameLower = "franck",
        uid="bodum",
        secondaryUid="f.bodum",
        domain="example",
        domainExtension="org"
    ))

    print("Starting tmpcontainer...")
    container = docker.run("-d", "-h", settings.HOSTNAME, "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro", "-v", "{}/{}/:/data/".format(basedir, dataset), tmpname).rstrip()

    # Wait for imap to become available on imaps://localhost:993
    time.sleep(5)

    print("Running populate.sh...")
    docker("exec", container,  "/data/populate.sh", _out=process_output)

    print("Comitting results to: {}".format(imagename))
    docker.commit(container, imagename)
    docker.stop(container)
    docker.rm(container)
