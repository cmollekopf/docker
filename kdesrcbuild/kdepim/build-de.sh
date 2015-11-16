#! /bin/sh
#cd /work/source
#git clone https://github.com/kolab-groupware/kde-l10n-de.git
#git checkout kolab/dev
#cd kde-l10n-de
#./scripts/autogen.sh de

mkdir -p /work/build/kde-l10n-de
cd /work/build/kde-l10n-de
cmake -DCMAKE_INSTALL_PREFIX=/work/install /work/source/kde-l10n-de/de
make
make install
