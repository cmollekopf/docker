#!/bin/bash
docker run --rm -ti -p 80:80 -p 143:143 -p 443:443 -p 587:587 -p 4190:4190 -h kolab1.dev.local -v /sys/fs/cgroup:/sys/fs/cgroup:ro kolab1:ready bash
