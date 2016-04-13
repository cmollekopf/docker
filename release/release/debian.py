# -*- coding: utf-8 -*-
"""
    Handles debian repos via python.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2016-04-13
    Copyright: GPL-2+
"""

import os
import re

from debian import changelog

from . import config, cd

class DebianPackage:
    def __init__(self, path, package):
        self.path = os.path.abspath(path)
        self.name = package.package
        self.upstream_version = package.upstream_version
        self.base_version = re.search("^([0-9\.]+:)?(?P<version>[0-9\.]+)(\+|~|$)", package.upstream_version).group("version")
        self.version = package.version

    def dscPath(self):
        version = self.upstream_version +"-"+ self.version.debian_version
        return os.path.abspath("%s/../%s_%s.dsc" % (self.path, self.name, version))

    def origPath(self, version=None):
        if not version:
            version = self.upstream_version
        return os.path.abspath("%s/../%s_%s.orig.tar.gz" % (self.path, self.name, version))

    def setGitBuild(self, upstream, branch):
        self.upgrade(upstream.gitVersion(self, branch), "git build of %s"%upstream.gitHash(self, branch))

    def upgrade(self, upstream_version, msg):
        self.upstream_version = upstream_version
        version = "%s-0~kolab1" % self.upstream_version

        try:
            version = config.epoch[self.name] + version
        except KeyError:
            pass

        with cd(self.path):
            os.system('DEBEMAIL="{}" DEBFULLNAME="{} {}"  dch -v {} "{}"'.format(
                config.mail, config.name, config.comment, version, msg).encode("utf-8")
                )
            os.system('DEBEMAIL="{}" DEBFULLNAME="{} {}"  dch -r ""'.format(
                config.mail, config.name, config.comment).encode("utf-8")
                )
            c = changelog.Changelog(open("debian/changelog", encoding="utf-8").read())
            self.version = c.version
            self.upstream_version = c.upstream_version
            self.base_version = re.search("^([0-9\.]+:)?(?P<version>[0-9\.]+)(\+|~|$)", c.upstream_version).group("version")

    def createDsc(self):
        with cd("%s/.." % self.path):
            os.system('DEBEMAIL="{}" DEBFULLNAME="{} {}" dpkg-source -b {}'.format(config.mail, config.name, config.comment, self.name).encode("utf-8"))

def debianPackage(name):
    base = os.path.join(config.debianBase, name)
    c = changelog.Changelog(open(os.path.join(base,'debian/changelog'), encoding="utf-8").read())
    return DebianPackage(base, c)
