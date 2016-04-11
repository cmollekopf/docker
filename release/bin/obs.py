#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Handles obs via python.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2016-04-11
    Copyright: GPL-2+
"""


from debian import changelog
from git import Repo

import os
import re
import shutil
import tarfile
import contextlib

from release import getPackage

from datetime import datetime, timedelta, tzinfo
import time as _time

ZERO = timedelta(0)
STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

Local = LocalTimezone()


EXCEPT = ("kde-build-metadata", "log",
          "kdelibs", "kfilemetadata",
          "libkolab", "libkolabxml",
          "kde-l10n-de",
          )       #dirs to except

EPOCH={"kdepim-runtime": "4:",
        "kdepim": "4:",
        "kdepimlibs": "4:",
        "kfilemetadata": "4:",
        "baloo": "4:",
        }

@contextlib.contextmanager
def cd(path):
   old_path = os.getcwd()
   os.chdir(path)
   try:
       yield
   finally:
       os.chdir(old_path)

class ObsRepo:
    tomove = ['rules','control','changelog']

    def __init__(self, base):
        self.base = base

    def packageDir(self, package):
        """return the folder of the obsi for a package"""
        return "%s/%s" %(self.base, package.name)

    def fromObs(self, package):
        os.system("tar -xaf %s/debian.tar.gz"%(self.packageDir(package)))
        for i in self.tomove:
            shutil.copy("%s/debian.%s"%(self.packageDir(package), i), "debian/%s"%i)

    def toObs(self, package):
        self.createDsc(package)
        self.createDebianTar(package)
        self.move2Obs(package)

    def createDsc(self, package):
        files = ["%s-%s.orig.tar.gz"%(package.name,package.upstream_version), "debian.tar.gz"]
        package.createDsc()
        content = open(package.dscPath()).read()

        content = re.sub(r"^-----BEGIN PGP SIGNED MESSAGE-----\nHash.*\n+", "", content)
        content = re.sub(r"\n+-----BEGIN PGP SIGNATURE-----\n.*-----END PGP SIGNATURE-----", "", content, flags=re.M+re.S)
        content = re.sub(r"^Format: .*$", "Format: 1.0", content, flags=re.M)
        content = re.sub("^(Checksums.*|Files):\s*\n( .*\n)+","", content, flags=re.M)
        content =  "%sFiles:\n%s"%(content.decode('utf8'),"\n".join([" 00000000000000000000000000000000 0 %s"%i for i in files]))

        with open("%s/%s.dsc"%(self.packageDir(package), package.name),'w') as f:
            f.write(content.encode('utf8'))

    def createDebianTar(self, package):
        def exclude(fname):
            if os.path.basename(fname) in self.tomove+['source']:
                return True
            else:
                return False
        with cd(package.path):
            with tarfile.open("%s/debian.tar.gz"%(self.packageDir(package)), "w:gz") as t:
                t.add("debian",exclude=exclude)

    def move2Obs(self, package):
        with cd(package.path):
            for i in self.tomove:
                shutil.copy("debian/"+i, "%s/debian.%s"%(self.packageDir(package), i))
            if not self.base.endswith(":Git"):
                self.copyOrig(package, package.upstream_version)

    def releaseSpec(self, package, version):
        self.addChangelogEntryFedora(package, version)
        with cd(self.packageDir(package)):
            with open("%s.spec" % package.name) as f:
                content = f.read()
            content = re.sub(r"(?P<vStr>\n\s*Version:\s*)[0-9.:]+\s*\n", r"\g<vStr>{v}\n".format(v=version), content)
            with open("%s.spec" % package.name, "w") as f:
                f.write(content)

    def releaseDsc(self, package, version):
         self.addChangelogEntryDebian(package, version)
         with cd(self.packageDir(package)):
            with open("%s.dsc" % package.name) as f:
                content = f.read()
            content = re.sub(r"(?P<vStr>\n\s*Version:\s*)[0-9.:\-~a-z]+\s*\n", r"\g<vStr>{epoch}{v}-0~kolab1\n".format(epoch=EPOCH.get(package.name, ""),v=version), content)
            with open("%s.dsc" % package.name, "w") as f:
                f.write(content)

    def addChangelogEntryFedora(self, package, version):

        c = "* {date} {author} - {v}-1\n- New upstream release {v}\n".format(
                                date = datetime.now(Local).strftime("%a %b %d %Y"),
                                author = "Sandro Knauß (Kolab Systems) <knauss@kolabsys.com>",
                                v = version
                                )

        with cd(self.packageDir(package)):
            with open("%s.spec" % package.name) as f:
                content = f.read()

            lastupdate = re.search(r"\n\s*%changelog(\s*\n)+.* - (?P<version>[0-9\.]+)(-[0-9]+)?\n", content).group("version")
            if (lastupdate != version) :
                content = re.sub(r"(\n\s*%changelog\s*\n)", r"\1{c}\n".format(c=c), content)
                with open("%s.spec" % package.name, "w") as f:
                    f.write(content)

    def addChangelogEntryDebian(self, package, version):
        fname = "{path}/debian.changelog".format(path=self.packageDir(package))
        c = changelog.Changelog(open(fname).read())
        if (c.upstream_version != version):
            c.new_block(package=package.name,
                        version="{epoch}{v}-0~kolab1".format(epoch=EPOCH.get(package.name, ""),v=version),
                        distributions="unstable", urgency="medium",
                        author="Sandro Knauß (Kolab Systems) <knauss@kolabsys.com>",
                        date=datetime.now(Local).strftime("%a, %d %b %Y %H:%M:%S %z"),
                        changes=["","  * New upstream release {v}".format(v=version),""]
                        )
            c.write_to_open_file(open(fname, "w"))

    def debianUpstreamVersion(self, package):
        fname = "{path}/debian.changelog".format(path=self.packageDir(package))
        c = changelog.Changelog(open(fname).read())
        return c.upstream_version

    def copyOrig(self, package, version):
            shutil.copy(package.origPath(version), self.packageDir(package))

    def updateSourceSpec(self, package):
        with cd(self.packageDir(package)):
            with open("%s.spec" % package.name) as f:
                content = f.read()
            content = re.sub(r"(?P<vSource>\n\s*Source0:\s*).*\n", r"\g<vSource>%{name}_%{version}.orig.tar.gz\n", content)
            with open("%s.spec" % package.name, "w") as f:
                f.write(content)

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
            version = EPOCH[self.name] + version
        except KeyError:
            pass

        with cd(self.path):
            os.system('DEBEMAIL="knauss@kolabsys.com" dch -v %s "%s"' %
                (version, msg)
                )
            c = changelog.Changelog(open("debian/changelog").read())
            self.version = c.version
            self.upstream_version = c.upstream_version
            self.base_version = re.search("^([0-9\.]+:)?(?P<version>[0-9\.]+)(\+|~|$)", c.upstream_version).group("version")

    def createDsc(self):
        with cd("%s/.." % self.path):
            os.system('DEBEMAIL="knauss@kolabsys.com" dpkg-source -b %s' % (self.name))


#dest="/home/hefee/kolab/obs/Kontact:4.13:Development/"

def update(repoBase, debianBase, obsBase):
    """push updates to OBS"""

    obs = ObsRepo(obsBase)

    projects = os.walk(repoBase).next()[1]

    for p in projects:
        if p in EXCEPT:
            continue
        pkg = getPackage(p, repoBase, debianBase)
        pkg.repo.remotes.origin.fetch()
        version = pkg.newestVersion()
        if (version != obs.debianUpstreamVersion(pkg)):
            print("{} {}...".format(pkg.name, version))
            try:
                os.stat(pkg.origPath(version))
            except OSError:
                pkg.createGitTar(version)
            obs.copyOrig(pkg, version)
            obs.releaseSpec(pkg, version)
            obs.releaseDsc(pkg, version)


repoBase = "/work/source"
debianBase = "/work/debian"
obsBase = "/work/obs/Kontact:4.13:Development"

repo = ObsRepo(obsBase)

def debianPackage(name):
    base = os.path.join(debianBase,name)
    c = changelog.Changelog(open(os.path.join(base,'debian/changelog')).read())
    return DebianPackage(base, c)

#if __name__ == "__main__":
#    update("/work/source", os.path.abspath(os.path.expanduser("~kdetest/kde/debian/")), "/home/hefee/kolab/obs/Kontact:4.13:Development/")

#p = getPackage("akonadi", "/work/source/", os.path.abspath("."))
