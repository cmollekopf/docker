#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Push changes from debian repo to obs.

    Call like this:

    pushtoobs.py baloo kolab/Ubuntu_14.04+ Kontact:4.13:Development

    this will update baloo Kontact:4.13:Development OBS from the debian repo

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

print("syncing %s(%s) to %s"%(p, branch, obsName))
pkg = package.getPackage(p, repoBase, debianBase)

deb = debian.debianPackage(p)
debRepo = Repo(deb.path)

if not branch in deb.branches():
    sys.exit("Unknown branch %s - only allowed: %s"%(branch, deb.branches()))

debRepo.heads[branch].checkout()
#we need to updte the variables, because the version is only read once
pkg = package.getPackage(p, repoBase, debianBase)
deb = debian.debianPackage(p)

obsrepo.toObs(deb, branch)

print("OBS is now updated from debian repo")
