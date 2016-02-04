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
       return [
           "-e", "DISPLAY={}".format(self.DISPLAY),
           "-e", "XAUTHORITY={}".format(self.XAUTH),
           "-v", "{}:{}".format(self.XAUTH, self.XAUTH),
           "-v", "/tmp/.X11-unix:/tmp/.X11-unix",
	   "--device", "/dev/dri/card0:/dev/dri/card0",
	   "--device", "/dev/dri/renderD128:/dev/dri/renderD128",
	   "--device", "/dev/dri/controlD64:/dev/dri/controlD64",
       ]
