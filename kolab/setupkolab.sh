#!/bin/bash
#assumes the container is running
LDIFFILE=/doe.ldif
LDAPPW=test
docker run -d -h kolab1.example.org -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $(pwd)/doe.ldif:$LDIFFILE kolab1:latest
sleep 1
echo "Running setup-kolab... "
CONTAINER=$(docker ps -a | grep kolab1:latest | head -n 1 | awk '{ print $1 }')
echo "Container: $CONTAINER"
docker exec $CONTAINER setup-kolab --default --timezone=Europe/Brussels --directory-manager-pwd=$LDAPPW --mysqlserver=new

echo "Adding default user: doe@example.org Welcome2KolabSystems"
docker exec $CONTAINER ldapadd -x -h localhost -D "cn=Directory Manager" -w $LDAPPW -f $LDIFFILE
docker commit $CONTAINER kolab/kolabtestcontainer:latest
docker stop $CONTAINER
docker rm $CONTAINER

