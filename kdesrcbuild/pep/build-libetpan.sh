#!/bin/bash
export CPATH=/work/install/include/
export LIBRARY_PATH=/work/install/lib/
export LD_LIBRARY_PATH=/work/install/lib/
mkdir ~/lib/
cd /work/source/libetpan/
./configure --prefix=/work/install
make install
