# -*- coding: utf-8 -*-
"""
    Handles obs via python.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2016-04-11
    Copyright: GPL-2+
"""


from debian import changelog

import glob
import os
import re
import shutil
import subprocess
import tarfile
import contextlib

from . import config, cd

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

class ObsRepo:
    tomove = ['rules','control','changelog']

    def __init__(self, base):
        self.base = base

    def packageDir(self, package):
        """return the folder of the obsi for a package"""
        return "%s/%s" %(self.base, package.name)

    def fromObs(self, package):
        with cd(package.path):
            os.system("tar -xaf %s/debian.tar.gz"%(self.packageDir(package)))
            for i in self.tomove:
                fname = "debian/%s"%i
                shutil.copy("%s/debian.%s"%(self.packageDir(package), i), fname)
                os.chmod(fname, 0o644)

    def toObs(self, package):
        self.createDsc(package)
        self.createDebianTar(package)
        self.move2Obs(package)

    def createDsc(self, package):
        files = ["%s-%s.orig.tar.gz"%(package.name,package.upstream_version), "debian.tar.gz"]
        package.createDsc()
        content = open(package.dscPath(), encoding="utf-8").read()

        content = re.sub(r"^-----BEGIN PGP SIGNED MESSAGE-----\nHash.*\n+", "", content)
        content = re.sub(r"\n+-----BEGIN PGP SIGNATURE-----\n.*-----END PGP SIGNATURE-----", "", content, flags=re.M+re.S)
        content = re.sub(r"^Format: .*$", "Format: 1.0", content, flags=re.M)
        content = re.sub("^(Checksums.*|Files):\s*\n( .*\n)+","", content, flags=re.M)
        content =  "%sFiles:\n%s"%(content,"\n".join([" 00000000000000000000000000000000 0 %s"%i for i in files]))

        with open("%s/%s.dsc"%(self.packageDir(package), package.name),'w', encoding="utf-8") as f:
            f.write(content)

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
            with open("%s.spec" % package.name, encoding="utf-8") as f:
                content = f.read()
            content = re.sub(r"(?P<vStr>\n\s*Version:\s*)[0-9.:]+\s*\n", r"\g<vStr>{v}\n".format(v=version), content)
            with open("%s.spec" % package.name, "w", encoding="utf-8") as f:
                f.write(content)

    def releaseDsc(self, package, version):
         self.addChangelogEntryDebian(package, version)
         with cd(self.packageDir(package)):
            for fname in glob.glob("%s*.dsc" % package.name):
                with open(fname, encoding="utf-8") as f:
                    content = f.read()
                preVersion = config.epoch.get(package.name, "")
                try:
                    preVersion = re.search(r"\n\s*Version:\s*([0-9.:\-~a-z]+\+really).*\n", content).group(1)
                except AttributeError:
                    pass

                content = re.sub(r"(?P<vStr>\n\s*Version:\s*)[0-9.:\-~a-z\+]+\s*\n", r"\g<vStr>{pv}{v}-0~kolab1\n".format(pv=preVersion,v=version), content)
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(content)


    def addChangelogEntryFedora(self, package, version):

        c = "* {date} {author} - {v}-1\n- New upstream release {v}\n".format(
                                date = datetime.now(Local).strftime("%a %b %d %Y"),
                                author = "{} {} <{}>".format(config.name, config.comment, config.mail),
                                v = version
                                )

        with cd(self.packageDir(package)):
            with open("%s.spec" % package.name, encoding="utf-8") as f:
                content = f.read()

            lastupdate = re.search(r"\n\s*%changelog(\s*\n)+.* - (?P<version>[0-9\.]+)(-[0-9]+)?\n", content).group("version")
            if (lastupdate != version) :
                content = re.sub(r"(\n\s*%changelog\s*\n)", r"\1{c}\n".format(c=c), content)
                with open("%s.spec" % package.name, "w", encoding="utf-8") as f:
                    f.write(content)

    def addChangelogEntryDebian(self, package, version):
        fname = "{path}/debian.changelog".format(path=self.packageDir(package))
        c = changelog.Changelog(open(fname, encoding="utf-8").read())
        if (c.upstream_version != version):
            c.new_block(package=package.name,
                        version="{epoch}{v}-0~kolab1".format(epoch=config.epoch.get(package.name, ""),v=version),
                        distributions="unstable", urgency="medium",
                        author="{} {} <{}>".format(config.name, config.comment, config.mail),
                        date=datetime.now(Local).strftime("%a, %d %b %Y %H:%M:%S %z"),
                        changes=["","  * New upstream release {v}".format(v=version),""]
                        )
            c.write_to_open_file(open(fname, "w", encoding="utf-8"))

    def debianUpstreamVersion(self, package):
        fname = "{path}/debian.changelog".format(path=self.packageDir(package))
        c = changelog.Changelog(open(fname, encoding="utf-8").read())
        return c.upstream_version

    def copyOrig(self, package, version):
            shutil.copy(package.origPath(version), self.packageDir(package))

    def updateSourceSpec(self, package):
        with cd(self.packageDir(package)):
            with open("%s.spec" % package.name, encoding="utf-8") as f:
                content = f.read()
            content = re.sub(r"(?P<vSource>\n\s*Source0:\s*).*\n", r"\g<vSource>%{name}_%{version}.orig.tar.gz\n", content)
            with open("%s.spec" % package.name, "w", encoding="utf-8") as f:
                f.write(content)

    def update(self, package):
       with cd(self.packageDir(package)):
           return os.system('osc update')

    def status(self, package):
       with cd(self.packageDir(package)):
           status = subprocess.Popen(["osc", "status"], stdout=subprocess.PIPE).communicate()[0]
           return [i.split(b"    ") for i in status.splitlines()]

    def commit(self, package, message):
       with cd(self.packageDir(package)):
           return os.system('osc commit -m "{}"'.format(message))

    def add(self, package, fname):
       with cd(self.packageDir(package)):
           return os.system('osc add {}'.format(fname))

    def remove(self, package, fname):
       with cd(self.packageDir(package)):
           return os.system('osc remove {}'.format(fname))

