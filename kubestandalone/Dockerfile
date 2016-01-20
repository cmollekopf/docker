FROM fedora:22

RUN yum install -y xerces-c boost
RUN yum install -y sudo
RUN yum install -y cyrus-sasl cyrus-sasl-plain
RUN yum install -y gtk2
RUN yum install -y qt-common vim
RUN yum install -y libnotify libxdg-basedir
RUN yum install -y mesa-dri-drivers xorg-x11-drv-intel

#AkonadiNext deps
RUN yum -y install qt5-qtbase libgit2 lmdb
RUN yum -y install xterm

#Test debugging
RUN yum -y install gdb

#Frameworks
RUN yum -y install qt5-qtscript qt5-qttools qt5-qtsvg qt5-qtx11extras xcb-util-keysyms qt5-qttools-static polkit qt5-qtdeclarative libepoxy qt5-qtwebkit qt5-qtxmlpatterns

#Debug deps
RUN yum -y install gdb

RUN yum install -y qt5-qtbase
RUN yum install -y kf5-ki18n kf5-kcodecs
RUN yum -y install kf5-kpackage
RUN yum -y install dbus-x11

#qmlscene
RUN yum -y install qt5-qtdeclarative-devel
#kube
RUN yum -y install qt5-qtquickcontrols
RUN yum -y install kf5-plasma
RUN yum -y install oxygen-icon-theme
RUN yum -y install gamin

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

ADD entrypoint.sh /home/developer/entrypoint.sh
ADD bashrc /home/developer/.bashrc

#Fix ping
RUN sudo setcap cap_net_raw+ep /usr/bin/ping

RUN sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime

RUN sudo dbus-uuidgen --ensure

USER developer
ENV HOME /home/developer
CMD /bin/bash
