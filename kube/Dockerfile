FROM cmollekopf/fedora:25

RUN dnf install -y xerces-c boost
RUN dnf install -y sudo
RUN dnf install -y cyrus-sasl cyrus-sasl-plain
RUN dnf install -y gtk2
RUN dnf install -y qt-common
RUN dnf install -y libnotify libxdg-basedir
RUN dnf install -y mesa-dri-drivers xorg-x11-drv-intel

#Sink deps
RUN dnf -y install qt5-qtbase libgit2 lmdb
RUN dnf -y install xterm

#Test debugging
RUN dnf -y install gdb

#Frameworks
RUN dnf -y install qt5-qtscript qt5-qttools qt5-qtsvg qt5-qtx11extras xcb-util-keysyms qt5-qttools-static polkit qt5-qtdeclarative libepoxy qt5-qtwebkit qt5-qtxmlpatterns

RUN dnf install -y qt5-qtbase
RUN dnf install -y kf5-ki18n kf5-kcodecs
RUN dnf -y install kf5-kpackage
RUN dnf -y install dbus-x11

#For kirigami
RUN dnf -y install qt5-qtgraphicaleffects

#qmlscene
RUN dnf -y install qt5-qtdeclarative-devel
#kube
RUN dnf -y install qt5-qtquickcontrols qt5-qtquickcontrols2
RUN dnf -y install kf5-plasma
RUN dnf -y install oxygen-icon-theme
RUN dnf -y install gamin
RUN dnf -y install qt5-qtwebengine
RUN dnf -y install qt5ct plasma-breeze google-noto-serif-fonts google-noto-sans-fonts
RUN dnf -y install gnupg2-smime pinentry-qt

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
WORKDIR /home/developer/
CMD /bin/bash
