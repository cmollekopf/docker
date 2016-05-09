#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  Search and perform an update for all repos.

  Copyright: Sandro Knauß <knauss@kolabsys.com>
  Date: 2016-04-11
  Copyright: GPL-2+
"""

import os, glob, re
from git import Repo, Actor

from release import obs, config, package, debian, cd

EXCEPT = ("kde-build-metadata", "log",
      "kdelibs", "kfilemetadata",
      "kde-l10n-de",
      )     #dirs to except

def release(repoBase, debianBase):
  """search for uncommited repos and release a new version"""

  projects = next(os.walk(repoBase))[1]

  actor = Actor("{} {}".format(config.name, config.comment), config.mail)

  for p in projects:
    if p in EXCEPT:
      continue
    pkg = package.getPackage(p, repoBase, debianBase)
    pkg.repo.remotes.origin.fetch()
    newestTag = pkg.newestTag()
    log = pkg.repo.git.log('--pretty=format:%h - %an(%ar): %s','{}..origin/{}'.format(newestTag, pkg.branch))
    if not log:
        # print("{} is uptodate ({})".format(p, pkg.newestVersion()))
        continue

    print("{} ({}) has commits on top:\n{}\n".format(p, pkg.newestVersion(), log))
    t = re.match("(.*\.)(\d+)",newestTag)
    kolabversion = str(int(t.group(2)) + 1)
    newTag = t.group(1)+kolabversion
    ret = input("Do you want to release {} y/n?".format(pkg.version(newTag)))
    if ret.lower() != "y":
        continue

    if pkg.repo.index.diff(None):
        print("repo is not clean can't go on form here: {}".format(pkg.repo.git.status()))
        continue
    pkg.repo.heads[pkg.branch].checkout()
    pkg.repo.remotes.origin.pull()

    with cd(os.path.join(repoBase, p)):
        with open("CMakeLists.txt", encoding="utf-8") as f:
            content = f.read()
            content = re.sub(r"_VERSION_KOLAB\s+(?P<s1>\"|')?\s*\d+\s*(\"|')?\s*\)\s*\n", r"_VERSION_KOLAB \g<s1>{v}\g<s1>)\n".format(v=kolabversion), content)
        with open("CMakeLists.txt", "w", encoding="utf-8") as f:
            f.write(content)
        pkg.repo.index.add(["CMakeLists.txt"])
        pkg.repo.index.commit("Prepare release of {tag}".format(tag=newTag), author=actor, committer=actor)
        pkg.repo.create_tag(newTag)

if __name__ == "__main__":
    release(config.repoBase, config.debianBase)
