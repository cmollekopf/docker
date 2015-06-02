import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
HOSTNAME = "kolab1.example.org"
LDAPPW = "test"
TIMEZONE = "Europe/Brussels"
KDEROOT = os.path.expanduser('~') + '/kdebuild/fedora/install'
REPOSITORY = "kolab/kolabtestcontainer"

def kolabimagename(name):
    return "{c.REPOSITORY}:{name}".format(c=config, name=name)

def populatedTag(dataset):
    return "populated-" + dataset

class Config:
    def __init__(self, module):
        self.module = module

    def __getattr__(self, name):
        """for settings.NAME"""
        return getattr(self.module, name)

    def __getitem__(self, name):
        """for using settings as dict"""
        return getattr(self.module, name)

config = Config(__import__(__name__))
