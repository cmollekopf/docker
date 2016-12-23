FROM centos:centos7

MAINTAINER Christian Mollekopf <mollekopf@kolabsys.com>

# This should really be a part of the base image.
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

# To speed things up, disable fastestmirror.
RUN sed -r -i \
        -e 's/^enabled.*$/enabled = 0/g' \
        /etc/yum/pluginconf.d/fastestmirror.conf

# Avoid using a mirrorlist (use a transparent proxy and cache everything instead).
RUN sed -r -i \
        -e 's/^mirrorlist/#mirrorlist/g' \
        -e 's/^#baseurl/baseurl/g' \
        /etc/yum.repos.d/*.repo

# Add EPEL.
RUN yum -y install \
        epel-release && \
    yum clean all

# Add wget.
RUN yum -y install \
        wget && \
    yum clean all

# Add the EPEL key.
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7

# Add the Kolab:Winterfell repository.
RUN wget -q -O /etc/yum.repos.d/Kolab:Winterfell.repo \
    http://obs.kolabsys.com/repositories/Kolab:/Winterfell/CentOS_7/Kolab:Winterfell.repo

# Give the Kolab:Winterfell repository priority over everything else.
RUN echo "priority=60" >> /etc/yum.repos.d/Kolab:Winterfell.repo

# Add the Kolab:Winterfell key.
RUN rpm --import https://ssl.kolabsys.com/community.asc

# Make YUM obey priorities configured.
RUN yum -y install \
        yum-plugin-priorities && \
    yum clean all

# Install some debugging utilities.
RUN yum -y install \
        bind-utils \
        cyrus-imapd \
        cyrus-sasl-plain \
        git \
        lsof \
        net-tools \
        nmap-ncat \
        openldap-clients \
        psmisc \
        strace \
        telnet \
        traceroute \
        vim-enhanced && \
    yum clean all

RUN yum -y install kolab

ADD /functions.sh /functions.sh
ADD /entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# RUN systemctl enable httpd.service
# RUN systemctl enable amavisd.service
# RUN systemctl enable postfix.service mariadb.service dirsrv.target cyrus-imapd.service wallace.service kolabd.service kolab-saslauthd.service

EXPOSE 80 143 443 587 4190
ENTRYPOINT ["/usr/sbin/init"] 
# FROM kvaps/kolab

# FROM kolab/kt:latest

# #Work around error: unpacking of archive failed on file /usr/lib/python2.7/site-packages/icalendar-3.8.2-py2.7.egg-info: cpio: rename
# RUN rm -rf /usr/lib/python2.7/site-packages/icalendar-3.8.2-py2.7.egg-info

# #Some base image sets nodocs, which breaks roundcube.
# RUN sed -i -e "s/tsflags=nodocs/#tsflags=nodocs/g" /etc/yum.conf
# RUN dnf -y reinstall \*

# ENV container docker
# RUN dnf -y swap -- remove fakesystemd -- install systemd systemd-libs
# RUN dnf -y update; yum clean all; \
# (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
# rm -f /lib/systemd/system/multi-user.target.wants/*;\
# rm -f /etc/systemd/system/*.wants/*;\
# rm -f /lib/systemd/system/local-fs.target.wants/*; \
# rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
# rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
# rm -f /lib/systemd/system/basic.target.wants/*;\
# rm -f /lib/systemd/system/anaconda.target.wants/*;
# VOLUME [ "/sys/fs/cgroup" ]

# #Temporary workaround for packaging error to get freebusy working
# RUN dnf -y install php-Monolog

# RUN dnf -y install patch

# #Services
# RUN dnf -y install httpd
# RUN dnf -y uninstall vim-minimal
# RUN dnf -y install vim
# RUN yum clean all
# RUN systemctl enable httpd.service
# RUN systemctl enable amavisd.service
# RUN systemctl enable postfix.service mariadb.service dirsrv.target cyrus-imapd.service wallace.service kolabd.service kolab-saslauthd.service

# EXPOSE 80 143 443 587 4190

# # We can't run setup-kolab during the building process, run the command below and then commit the result
# # RUN setup-kolab --default --timezone=Europe/Brussels --directory-manager-pwd=test --mysqlserver=new

# ENTRYPOINT ["/usr/sbin/init"] 
