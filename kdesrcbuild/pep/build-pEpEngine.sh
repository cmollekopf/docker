#!/bin/bash
export CPATH=/work/install/include/
export LIBRARY_PATH=/work/install/lib/
export LD_LIBRARY_PATH=/work/install/lib/
mkdir ~/lib/
cd /work/source/pEpEngine/
make install
cp ~/lib/libpEpEngine.so /work/install/lib/
cp -R ~/include/pEp /work/install/include/
