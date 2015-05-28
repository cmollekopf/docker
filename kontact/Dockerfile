FROM fedora:21

RUN yum install -y kdelibs-webkit prison qjson libical xapian-core boost-program-options dbus-x11 grantlee xorg-x11-font* mariadb-server qt-mysql kde-runtime kde-style-oxygen
RUN yum install -y mesa-dri-drivers xorg-x11-drv-intel
RUN yum install -y oxygen-icon-theme oxygen-mono-fonts oxygen-sans-font
RUN yum install -y xerces-c boost
RUN yum install -y kwallet
RUN yum install -y sudo
RUN yum install -y cyrus-sasl cyrus-sasl-plain
RUN yum install -y gtk2
RUN yum install -y qt-common vim
RUN yum install -y libnotify libxdg-basedir

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

ADD kdeenv.sh /home/developer/kdeenv.sh
ADD setupdbus.sh /home/developer/setupdbus.sh
ADD entrypoint.sh /home/developer/entrypoint.sh
ADD bashrc /home/developer/.bashrc

ADD home/developer/.kde4src /home/developer/.kde4src
RUN chown developer:developer /home/developer/.kde4src -R

USER developer
ENV HOME /home/developer
CMD /bin/bash
