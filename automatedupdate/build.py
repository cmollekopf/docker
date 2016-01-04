#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import os
import sys

from settings import config
import settings

def main():
    containername="kolabclient/presice"

    print("Building kolabclient for Ubuntu 12.04...")
    docker.build("-t", containername, "{c.SCRIPT_DIR}/ubuntu/precise/.".format(c=config), _out=sys.stdout)

if __name__ == "__main__":
	main()
