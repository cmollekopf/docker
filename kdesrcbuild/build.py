#!/usr/bin/env python2
from sh import docker
import settings

def process_output(line):
    print(line)

def main():
    docker.build("-t", "fedora-kdedev", settings.SCRIPT_DIR+"/kdesrcbuild/", _out=process_output)
