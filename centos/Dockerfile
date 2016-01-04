FROM centos:7

RUN yum -y update
RUN yum -y install sudo wget
RUN yum -y install epel-release

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
# ADD bashrc /home/developer/.bashrc

#Fix ping
# RUN sudo setcap cap_net_raw+ep /usr/bin/ping

# RUN sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime

RUN cd /etc/yum.repos.d/ && wget http://obs.kolabsys.com:82/Kontact:/4.13:/Git/CentOS_7/Kontact:4.13:Git.repo && cd -
RUN yum -y install kolab-desktop-client

USER developer
ENV HOME /home/developer
CMD /bin/bash
