import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
HOSTNAME = "kolab1.example.org"
LDAPPW = "test"
TIMEZONE = "Europe/Brussels"
KDEROOT = os.path.expanduser('~') + '/kdebuild/fedora/install'
REPOSITORY = "kolab/kolabtestcontainer"

def kolabimagename(name):
    return "{}:{}".format(REPOSITORY, name)

def populatedTag(dataset):
    return "populated-" + dataset
