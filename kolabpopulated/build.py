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

def main(dataset):
    tmpname="kolab/kolabtestcontainer:tmppopulated"
    imagename="kolab/kolabtestcontainer:populated-"+dataset
    basedir =  "{c.SCRIPT_DIR}/kolabpopulated".format(c=config)

    print("Building tmpcontainer...")
    docker.build("-t", tmpname, "{basedir}/.".format(basedir=basedir))

    print("Starting tmpcontainer...")
    container = docker.run("-d", "-h", settings.HOSTNAME,
            "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
            "-v", "{basedir}/{dataset}/:/data/".format(basedir=basedir, dataset=dataset),
            '-v',  "{c.SCRIPT_DIR}/kolab/populate/:/populate".format(c=config),
            tmpname).rstrip()
    try:
        # Wait for imap to become available on imaps://localhost:993
        time.sleep(5)

        print "Populate OU..."
        docker("exec", container, "python2", "/populate/populate_ou.py", _out=process_output)

        print "Populate users..."
        docker("exec", container, "python2", "/populate/populate_users.py", _out=process_output)

        print "Populate resources..."
        docker("exec", container, "python2", "/populate/populate_resources.py", _out=process_output)

        print("Running populate.sh...")
        docker("exec", container,  "/data/populate.sh", _out=process_output)

        # Give kolabd some time to create all mailboxes
        time.sleep(5)

        docker("exec", container, "patch", "-R", "/etc/kolab/kolab.conf", "/data/kolab.conf.diff", _out=process_output)
        docker("exec", container, "patch", "-R", "/etc/roundcubemail/calendar.inc.php", "/data/calendar.inc.php.diff", _out=process_output)
        docker("exec", container, "patch", "-R", "/etc/roundcubemail/config.inc.php", "/data/config.inc.php.diff", _out=process_output)
        docker("exec", container, "patch", "-R", "/etc/roundcubemail/kolab_addressbook.inc.php", "/data/kolab_addressbook.inc.php.diff", _out=process_output)
        docker("exec", container, "patch", "-R", "/etc/roundcubemail/kolab_auth.inc.php", "/data/kolab_auth.inc.php.diff", _out=process_output)
        docker("exec", container, "patch", "-R", "/etc/roundcubemail/password.inc.php", "/data/password.inc.php.diff", _out=process_output)

        print("Comitting results to: {}".format(imagename))
        docker.commit(container, imagename)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        print("Failed to setup container")

    docker.stop(container)
    docker.rm(container)
