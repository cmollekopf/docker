FROM fedora:22

RUN yum -y update
RUN yum -y install wget sed sudo gpg

RUN cd /etc/yum.repos.d/ && wget https://obs.kolabsys.com/repositories/Kontact:/4.13:/Git/Fedora_22/Kontact:4.13:Git.repo

RUN for f in /etc/yum.repos.d/Kontact*.repo; do sed -i "s#enabled=1#enabled=1\\npriority=0#g" $f; done

RUN gpg --keyserver keys.gnupg.net --recv-keys 446D5A45
# RUN gpg --search devel@lists.kolab.org
RUN gpg --export --armor devel@lists.kolab.org > devel.asc
RUN rpm --import devel.asc

RUN yum -y install kde-runtime
RUN yum -y install kolab-desktop-client

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

USER developer
ENV HOME /home/developer
CMD /bin/bash
