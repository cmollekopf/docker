#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Pull changes from obs to debian repo.

    Call like this:

    pullfromobs.py baloo kolab/Ubuntu_14.04+ Kontact:4.13:Development

    this will update baloo the kolab/Ubuntu_14.04+ branch from Kontact:4.13:Development OBS

    Copyright: Sandro Knauß <knauss@kolabsys.com>
    Date: 2017-01-23
    Copyright: GPL-2+
"""

import sys
from git import Repo
from release import obs, config, package, debian

repoBase = config.repoBase
debianBase = config.debianBase

p = sys.argv[1] # package name
branch = sys.argv[2] # branch to sync
obsName = sys.argv[3]

obsrepo = obs.ObsRepo("/work/osc/" + obsName)

print("syncing %s(%s) from %s"%(p, branch, obsName))
pkg = package.getPackage(p, repoBase, debianBase)

deb = debian.debianPackage(p)
debRepo = Repo(deb.path)

if not branch in deb.branches():
    sys.exit("Unknown branch %s - only allowed: %s"%(branch, deb.branches()))

#update obs
if obsrepo.update(deb) != 0:
        sys.exit("obs update failed - please fix yourself")

if obsrepo.status(deb) != []:
        sys.exit("obs status shows a diff - please fix yourself")

#update branch on debian repo
if not branch in debRepo.heads:
   debRepo.create_head(branch, debRepo.remotes.origin.refs[branch]).set_tracking_branch(debRepo.remotes.origin.refs[branch])
debRepo.heads[branch].checkout()
debRepo.remotes.origin.pull()
if debRepo.index.diff(None):
    sys.exit("There are changes in obs that are not part of git - Please commit your changes")

# push changes from obs to git
obsrepo.fromObs(deb, branch)

print("Debian repo is now updated from obs")
