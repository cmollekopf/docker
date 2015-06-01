#!/usr/bin/env python2
import sh
import subprocess

def findContainer(name):
    container=""
    try:
        container = sh.awk("{print $1}", _in=sh.head("-n 1", _in=sh.grep(name, _in=sh.docker.ps())))
    except:
        print "container not available"
    return container.rstrip()

def findImage(repository, tag):
    container=""
    try:
        container = sh.awk("{print $3}", _in=sh.head("-n 1", _in=sh.grep(tag, _in=sh.docker("images", repository))))
    except:
        print "container not available"
    return container.rstrip()
