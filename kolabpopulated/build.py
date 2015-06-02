#!/usr/bin/env python2
from sh import docker
import subprocess
import time
import os
import sys
import traceback

import settings
from settings import config

def process_output(line):
    print(line)

def generateUserFiles(template, outputfile, templateParams):
    with open(template) as f:
        data = f.read()

    with open(outputfile, "w") as f:
        data = data.format(**templateParams)
        f.write(data)

def prepareEnv(basedir):
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


def main(dataset):
    tmpname="kolab/kolabtestcontainer:tmppopulated"
    imagename="kolab/kolabtestcontainer:populated-"+dataset
    basedir =  "{c.SCRIPT_DIR}/kolabpopulated".format(c=config)

    print("Building tmpcontainer...")
    docker.build("-t", tmpname, "{basedir}/.".format(basedir=basedir))

    prepareEnv(basedir)

    print("Starting tmpcontainer...")
    container = docker.run("-d", "-h", settings.HOSTNAME,
            "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
            "-v", "{basedir}/{dataset}/:/data/".format(basedir=basedir, dataset=dataset),
            '-v',  "{c.SCRIPT_DIR}/kolab/populate/:/populate".format(c=config),
            tmpname).rstrip()
    try:
        # Wait for imap to become available on imaps://localhost:993
        time.sleep(5)

        print "Running populate_ou.py"
        docker("exec", container, "python2", "/populate/populate_ou.py", _out=process_output)

        print "Running populate_users.py"
        docker("exec", container, "python2", "/populate/populate_users.py", _out=process_output)

        print "Running populate_resources.py"
        docker("exec", container, "python2", "/populate/populate_resources.py", _out=process_output)

        print("Running populate.sh...")
        docker("exec", container,  "/data/populate.sh", _out=process_output)
        #Set invitation policy
        docker("exec", container, "sed", "-i", "s/kolab_invitation_policy = .*/kolab_invitation_policy = ALL_SAVE_AND_FORWARD/", "/etc/kolab/kolab.conf", _out=process_output)

        # Give kolabd some time to create all mailboxes
        time.sleep(5)

        print("Comitting results to: {}".format(imagename))
        docker.commit(container, imagename)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        print("Failed to setup container")

    docker.stop(container)
    docker.rm(container)
