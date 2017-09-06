import os
import sh

class X11Support():
    def __init__(self):
       self.DISPLAY = os.environ.get('DISPLAY')
       self.XAUTH="/tmp/.docker.xauth"
     
    def setupX11Authorization(self):
       try:
          sh.touch(self.XAUTH)
       except:
          print("touch failed")
       sh.xauth(sh.sed(sh.xauth("nlist", self.DISPLAY), "-e", 's/^..../ffff/'), "-f", self.XAUTH, "nmerge", "-")

    def docker_args(self):
       args = [
           "-e", "DISPLAY={}".format(self.DISPLAY),
           "-e", "XAUTHORITY={}".format(self.XAUTH),
           "-e", "XDG_RUNTIME_DIR=/run/user/1000", #Not strictly for X11 only, but required for graphical applications to avoid warning
           "-v", "{}:{}".format(self.XAUTH, self.XAUTH),
           "-v", "/tmp/.X11-unix:/tmp/.X11-unix",
	   "--device", "/dev/dri/card0:/dev/dri/card0"
       ]
       if os.path.isfile("/dev/dri/controlD64"):
           args.extend(["--device", "/dev/dri/controlD64:/dev/dri/controlD64"])
       if os.path.isfile("/dev/dri/renderD128"):
           args.extend(["--device", "/dev/dri/renderD128:/dev/dri/renderD128"])
       if os.path.isfile("/dev/dri/renderD64"):
           args.extend(["--device", "/dev/dri/renderD64:/dev/dri/renderD64"])
       return args
