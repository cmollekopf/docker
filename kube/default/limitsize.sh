#!/bin/bash
#Create a 30MB loopback device and mount it as data directory

dd if=/dev/zero of=/home/developer/virtualfs bs=1024 count=30720
sudo mknod -m 0660 /dev/loop2 b 7 2
sudo losetup /dev/loop2 /home/developer/virtualfs
mkfs -t ext3 -m 1 -v /dev/loop2
sudo mount -t ext3 /dev/loop2 /home/developer/.local/share/sink/
sudo chown -R developer:developer /home/developer/.local/share/sink/
