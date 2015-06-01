#!/bin/bash
#assumes the container is running
source ./config.sh
LDIFFILE=/doe.ldif
LDIFFILE2=/jane.ldif
docker run -d -h $HOSTNAME -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $(pwd)$LDIFFILE:$LDIFFILE -v $(pwd)$LDIFFILE2:$LDIFFILE2 -v $(pwd)/fixRoundcubeT243.sh:/usr/share/roundcubemail/fixRoundcubeT243.sh $TMPREPO:latest
sleep 1
echo "Running setup-kolab... "
CONTAINER=$(docker ps -a | grep $TMPREPO:latest | head -n 1 | awk '{ print $1 }')
echo "Container: $CONTAINER"

echo "Setting up kolab"
docker exec $CONTAINER setup-kolab --default --timezone=Europe/Brussels --directory-manager-pwd=$LDAPPW --mysqlserver=new

echo "Fixing roundcube"
docker exec $CONTAINER bash /usr/share/roundcubemail/fixRoundcubeT243.sh
docker exec $CONTAINER systemctl restart httpd

docker commit $CONTAINER $REPONAME:$TAG
docker stop $CONTAINER
docker rm $CONTAINER

