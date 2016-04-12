#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Create tarballs out of git with different tag schema.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2015-06-12
    Copyright: GPL-2+
"""

import os
import re
import functools
from git import Repo

EXCEPT = ("kde-build-metadata", "log")       #dirs to except

#maximum version for packages
MAXVERSIONS = {"kdepimlibs":"4.13.1",
               "kdepim-runtime":"4.13.1",
               "kdepim":"4.13.1",
               "kdelibs": "4.13.1",
               "baloo":"4.13.1",
               "kfilemetadata":"4.13.1",
               "akonadi":"1.13.0",
               "akonadi-ldap-resource":"99",
               "zanshin":"99",
               "libkolab":"1.0.0",
               "libkolabxml":"1.2.0",
               }

def package(name):
    """returns package class based on know tag schema"""
    p2p = { "kfilemetadata": KDEPackage,
            "kdelibs": KDEPackage
            }

    if name in p2p:
        return p2p[name]
    else:
        return NormalPackage

def getPackage(name, repoBase, origBase):
    return package(name)(name, MAXVERSIONS[name], repoBase, origBase)

class Package:
    def __init__(self, name, maxVersion, repoBase, origBase):
        self.origBase = origBase
        self.name = name
        self.repo = Repo(os.path.join(repoBase,name))
        self.maxTag = self.tag(maxVersion)

    def tags(self):
        return [t for t in self.repo.tags if self.matchTag(t)]

    def versionCmp(self, tag1, tag2):
        v1 = self.version(tag1).split(".")
        v2 = self.version(tag2).split(".")
        for a,b in zip(v1,v2):
                ret = int(a) - int(b)
                if ret != 0:
                    return ret
        return 0

    def newestTag(self):
         tags = [t.name for t in self.tags() if self.versionCmp(t.name, self.maxTag) < 0]
         tags.sort(key=functools.cmp_to_key(self.versionCmp))
         return tags[-1]

    def newestVersion(self):
        tag = self.newestTag()
        return self.version(tag)

    def origPath(self, version):
        return os.path.abspath("{}/{}_{}.orig.tar.gz".format(self.origBase, self.name, version))

    def createGitTar(self, version):
        tag = self.tag(version)
        self.repo.archive(open(self.origPath(version), "wb"),
                treeish = tag,
                prefix="{}-{}/".format(self.name, version),
                format="tar.gz",
        )

class NormalPackage(Package):
    """tag = <name>-<VERSION>"""
    def tag(self, version):
        return "{}-{}".format(self.name, version)

    def matchTag(self, tag):
        return re.match("^{}-[0-9.]+$".format(self.name),tag.name)

    def version(self, tagStr):
        return tagStr.split("-")[-1]

class SimplePackage(Package):
    """tag = <VERSION>"""
    def tag(self, version):
        return version

    def matchTag(self, tag):
        return re.match("^[0-9.]+$", tag.name)

    def version(self, tagStr):
        return tagStr

class KDEPackage(Package):
    """tag = v<VERSION>"""
    def tag(self, version):
        return "v"+version

    def matchTag(self, tag):
        return re.match("^v[0-9.]+$", tag.name)

    def version(self, tagStr):
        return tagStr[1:]

def release(repoBase, origBase):
    """reacte targz out of all git repos in <repoBase> and save the origs in origBase"""
    projects = next(os.walk(repoBase))[1]

    for p in projects:
        if p in EXCEPT:
            continue
        pkg = getPackage(p, repoBase, origBase)
        #pkg.repo.remotes.origin.fetch()
        version = pkg.newestVersion()
        if not os.path.exists(pkg.origPath(version)):
                print("{} {}...".format(pkg.name, version))
                pkg.createGitTar(version)
        else:
                print("{} is up-to-date".format(pkg.name))

if __name__ == "__main__":
    from release import config
    release(os.path.abspath(os.path.expanduser(config.repoBase)), os.path.abspath(config.debianBase))
