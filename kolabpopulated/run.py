#!/usr/bin/env python2
import sh
from sh import docker

import settings

def ports(standalone):
    p = ["-p", "80:80"]

    if standalone:
        p += ["-p", "143:143",
         "-p", "443:443",
         "-p", "587:587",
         "-p", "4190:4190",
         "-p", "389:389",
        ]

    return p

def main(dataset, standalone=False):
    runargs = [
        "-d",
        "-h", settings.HOSTNAME,
        "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
    ]

    runargs += ports(standalone)
    runargs += [settings.kolabimagename(settings.populatedTag(dataset))]
    docker.run(*runargs)
