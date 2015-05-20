#!/bin/bash
source ./config.sh
docker build -t $TMPREPO .
./setupkolab.sh
