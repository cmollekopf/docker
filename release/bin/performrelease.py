#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Performs an update of all packages.

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2016-04-11
    Copyright: GPL-2+
"""

import os, glob
from git import Repo, Actor

from release import obs, config, package, debian, cd

EXCEPT = ("kde-build-metadata", "log",
          "kdelibs", "kfilemetadata",
          "libkolab", "libkolabxml", "baloo",
          "kde-l10n-de",
          )       #dirs to except

def update(repoBase, debianBase, obsBase):
    """push updates to OBS"""

    obsrepo = obs.ObsRepo(obsBase)

    projects = next(os.walk(repoBase))[1]

    branch = "kolab/dev"

    actor = Actor("{} {}".format(config.name, config.comment), config.mail)

    for p in projects:
        if p in EXCEPT:
            continue
        print(p)
        pkg = package.getPackage(p, repoBase, debianBase)
        pkg.repo.remotes.origin.fetch()
        version = pkg.newestVersion()

        deb = debian.debianPackage(p)
        debRepo = Repo(deb.path)

        #update kolab/dev branch
        if not branch in debRepo.heads:
           debRepo.create_head(branch, debRepo.remotes.origin.refs[branch]).set_tracking_branch(debRepo.remotes.origin.refs[branch])
        debRepo.heads[branch].checkout()
        debRepo.remotes.origin.pull()
        if debRepo.index.diff(None):
            print("There are changes in obs that are not part of git - Please commit your changes")
            continue

        try:
            os.stat(pkg.origPath(version))
        except OSError:
            pkg.createGitTar(version)

	#update obs
        if obsrepo.update(deb) != 0:
                print("obs update failed - please fix yourself")
                continue

        if obsrepo.status(deb) != []:
                print("obs status shows a diff - please fix yourself")
                continue

        # push changes from obs to git
        obsrepo.fromObs(deb)
        if debRepo.index.diff(None):
            print("debian repo is not clean can't go on form here: {}".format(debRepo.git.status()))
            ret = input("show diff y/n?")
            if ret.lower() == "y":
                print(debRepo.git.diff())
            ret = input("Overwrite changes in OBS y/n?")
            if ret.lower() == "y":
                debRepo.heads[branch].checkout(force=True)
                obsrepo.toObs(deb)
            else:
                print("You will have to change the problem by your own - skipping {} for further processing".format(pkg.name))
                continue

        deb = debian.debianPackage(p)
        if version > deb.upstream_version:
            print("Updating from {} to {}".format(deb.upstream_version, version))
            deb.upgrade(version, "New upstream release {v}".format(v=version))
            debRepo.index.add(["debian/changelog"])
            debRepo.index.commit("Release {v}".format(v=version), author=actor, committer=actor)
            obsrepo.move2Obs(deb)
            obsrepo.releaseDsc(deb, version)
            obsrepo.releaseSpec(pkg, version)
            obsrepo.addChangelogEntryFedora(pkg, version)
            with cd(obsrepo.packageDir(deb)):
                list(map(os.unlink, glob.iglob("*.orig.tar.*")))
            obsrepo.copyOrig(pkg, version)

        if obsrepo.status(deb) != []:
            for i in obsrepo.status(deb):
                status = i[0].decode("utf-8")
                fname = i[1].decode("utf-8")
                if os.path.splitext(fname)[0].endswith("orig.tar"):
                    if fname == os.path.basename(deb.origPath(deb.upstream_version)):
                        if status in ("?", "D"):
                            obsrepo.add(deb, fname)
                        else:
                            print("used orig.tar.gz - but strange status:", i)
                    else:
                        if status == "?":
                            with cd(obsrepo.packageDir(deb)):
                                os.unlink(fname)
                        elif status == "!":
                            obsrepo.remove(deb, fname)
                        else:
                            print("unused orig.tar.gz - but strange status:", i)
            if version > deb.upstream_version:
                obsrepo.commit(deb, "New upstream release {v}".format(v=version))
            else:
                obsrepo.commit(deb, "Pushed changes from debian git")



if __name__ == "__main__":
	update(config.repoBase, config.debianBase, config.obsBase)
