FROM kolab/kt:latest

#Some base image sets nodocs, which breaks roundcube.
RUN sed -i -e "s/tsflags=nodocs/#tsflags=nodocs/g" /etc/yum.conf
RUN yum -y reinstall \*

ENV container docker
RUN yum -y swap -- remove fakesystemd -- install systemd systemd-libs
RUN yum -y update; yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]

#Services
RUN yum -y install httpd
RUN yum -y install vim
RUN yum clean all
RUN systemctl enable httpd.service
RUN systemctl enable postfix.service mariadb.service dirsrv.target cyrus-imapd.service wallace.service kolabd.service kolab-saslauthd.service
RUN systemctl enable amavisd.service

EXPOSE 80 143 443 587 4190

# We can't run setup-kolab during the building process, run the command below and then commit the result
# RUN setup-kolab --default --timezone=Europe/Brussels --directory-manager-pwd=test --mysqlserver=new

ENTRYPOINT ["/usr/sbin/init"] 
