#!/usr/bin/env python2
import sh
from sh import docker

import settings

def main(dataset):
    runargs = (
        "-d",
        "-p", "80:80",
        # "-p", "143:143",
        # "-p", "443:443",
        # "-p", "587:587",
        # "-p", "4190:4190",
        "-h", settings.HOSTNAME,
        "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
        settings.kolabimagename(settings.populatedTag(dataset))
    )
    docker.run(*runargs)
