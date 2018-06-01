FROM fedora:28

RUN dnf -y install kdelibs-webkit prison qjson libical xapian-core boost-program-options dbus-x11 grantlee xorg-x11-font* mariadb-server qt-mysql kde-runtime
RUN dnf -y install mesa-dri-drivers xorg-x11-drv-intel
RUN dnf -y install xerces-c boost
RUN dnf -y install kwallet
RUN dnf -y erase vim-minimal
RUN dnf -y install sudo vim
RUN dnf -y install cyrus-sasl cyrus-sasl-plain
RUN dnf -y install gtk2
RUN dnf -y install qt-common
RUN dnf -y install libnotify libxdg-basedir
#So we have at least some icons in zanshin until we manage to figure out how to configure the theme properly
#Qt probably thinks we're gnome for some reason, which breaks QIconLoader
RUN dnf -y install gnome-icon-theme

#we need smime support
RUN dnf -y install gnupg2-smime pinentry-qt

#Debug deps
RUN dnf -y install gdb

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

#Fix ping
RUN sudo setcap cap_net_raw+ep /usr/bin/ping

RUN sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime

USER developer
ENV HOME /home/developer
CMD /bin/bash
