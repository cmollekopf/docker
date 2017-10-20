FROM fedora:25

RUN dnf -y install 'dnf-command(copr)'
RUN dnf -y copr enable @kdesig/qt-5.9

RUN dnf -y install xerces-c boost
RUN dnf -y install sudo
RUN dnf -y install cyrus-sasl cyrus-sasl-plain
RUN dnf -y install libnotify libxdg-basedir
RUN dnf -y install mesa-dri-drivers xorg-x11-drv-intel
RUN dnf -y install vim-minimal xterm gdb valgrind
RUN dnf -y install gnupg2-smime pinentry-qt qgpgme

#Sink deps
RUN dnf -y install qt5-qtbase libgit2 lmdb

#Frameworks
RUN dnf -y install qt5-qtquickcontrols qt5-qtquickcontrols2 qt5-qtwebengine qt5-qtsvg
RUN dnf -y install kf5-kpackage kf5-ki18n kf5-kcodecs kf5-kcontacts kf5-kmime
RUN dnf -y install dbus-x11

#qmlscenl
RUN dnf -y install qt5-qtdeclarative-devel

#kube
RUN dnf -y install google-noto-serif-fonts google-noto-sans-fonts
RUN dnf -y install qgpgme
RUN dnf -y install strace

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
