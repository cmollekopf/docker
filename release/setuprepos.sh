#!/bin/bash

#setup debian clone
mkdir -p /work/debian
cd /work/debian
for repo in libkolab libkolabxml akonadi akonadi-ldap-resource kdepimlibs kdepim kdepim-runtime baloo; do
	if [ ! -d /work/debian/$repo ]; then
		git clone github:kolab-groupware/debian-$repo $repo
	fi
done

# setup osc clone
mkdir -p /work/osc
cd /work/osc
for repo in Kontact:4.13:Development Kontact:4.13 Kontact:4.13:Git home:knauss:branches:Kontact:4.13:Git; do
	if [ ! -d /work/osc/$repo ]; then
		osc -A https://obs.kolabsys.com co $repo
	fi
done

cd 
