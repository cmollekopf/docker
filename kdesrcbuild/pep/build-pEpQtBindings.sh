#!/bin/bash
mkdir -p /work/build/pEpQtBindings
cd /work/build/pEpQtBindings
cmake -DCMAKE_INSTALL_PREFIX=/work/install /work/source/pEpQtBindings
make
make install
