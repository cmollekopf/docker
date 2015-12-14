#!/usr/bin/env python2
import sh
from sh import docker
import subprocess
import settings
import dockerutils
import argparse
from x11support import X11Support

from automatedupdate import BASEPATH

def main(x11forward):
    runargs = [ "-ti",
        "--rm",
        "--privileged",
        "-v", "~/kdebuild/automatedupdate:/work",
	"-v", "{}/bashrc:/home/developer/.bashrc".format(BASEPATH),
    ]
    if x11forward:
	    x11 = X11Support()
	    x11.setupX11Authorization()
	    runargs.extend(x11.docker_args())
    image="kolabclient:presice"
    runargs.append(image)
    runargs.extend(["-c","bash"])
    args = ["docker","run"]
    args.extend(runargs)
    subprocess.call(" ".join(args), shell=True, cwd=settings.SCRIPT_DIR)

if __name__ == "__main__":
	main(True)
