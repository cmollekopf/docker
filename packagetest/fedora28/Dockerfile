FROM fedora:28

RUN dnf -y update
RUN dnf -y install wget sed sudo gpg dnf-plugins-core

RUN echo "priority=1" >> /etc/dnf/dnf.conf

RUN dnf config-manager --add-repo=http://obs.kolabsys.com/repositories/Kontact:/4.13:/Development/Fedora_28/ --setopt priority=0 Kontact:4.13:Development_Fedora28


RUN wget https://obs.kolabsys.com/projects/Kontact:4.13:Development/public_key -O /tmp/key && rpm --import /tmp/key

RUN dnf -y install kde-runtime plasma-desktop fedora-obsolete-packages
RUN dnf -y install kolab-desktop-client zanshin
RUN dnf -y install kde-l10n-de langpacks-de
RUN dnf -y install rpmreaper


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

RUN sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime

RUN sudo dbus-uuidgen --ensure

ADD config/.kde4src /home/developer/.kde4src
RUN chown developer:developer /home/developer/.kde4src -R

USER developer
ENV HOME /home/developer
ENV LANG "de_DE.UTF-8"
CMD /bin/bash
