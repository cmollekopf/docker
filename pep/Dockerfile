FROM fedora:21

RUN yum install -y xerces-c boost
RUN yum install -y sudo
RUN yum install -y cyrus-sasl cyrus-sasl-plain
RUN yum install -y gtk2
RUN yum install -y qt-common vim
RUN yum install -y libnotify libxdg-basedir

#we need smime support
RUN yum install -y gnupg2-smime pinentry-qt

#Debug deps
RUN yum -y install gdb

RUN yum install -y qt5-qtbase

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

USER developer
ENV HOME /home/developer
CMD /bin/bash
