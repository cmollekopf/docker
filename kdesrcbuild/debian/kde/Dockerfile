FROM debian:jessie

RUN echo "Aquire::http { Proxy \"http://172.17.42.1:3142\" };\n" > /etc/apt/apt.conf.d/01proxy
RUN echo "Aquire::https{ Proxy \"https://\" };" >> /etc/apt/apt.conf.d/01proxy

RUN echo "deb-src http://httpredir.debian.org/debian/ jessie main non-free contrib" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y dist-upgrade
RUN apt-get -y install git
RUN apt-get -y build-dep kde4libs akonadi
RUN apt-get -y install libxml-perl libjson-perl
RUN apt-get -y install libsm-dev libpcre3-dev
RUN apt-get -y install xsltproc
RUN apt-get -y install sudo

RUN apt-get -y install libmysqld-dev

#kdepimlibs
RUN apt-get -y install libgpgme11-dev libboost-graph-dev libsasl2-dev libqjson-dev libical-dev libldap2-dev

#baloo
RUN apt-get -y install libxapian-dev

#libkolabxml
RUN apt-get -y install libboost-thread-dev libboost-system-dev xsdcxx libxerces-c-dev libcurl4-openssl-dev

#zanshin
RUN apt-get -y install libboost-dev libboost-regex-dev

RUN useradd -d /home/developer -m developer
RUN mkdir /work /qt
RUN chown developer /work /qt

# some symlinks in /root to handle sudo ./kdesrc-build
RUN ln -s /home/developer/.kdesrc-buildrc /root/.kdesrc-buildrc && \
    ln -s /home/developer/kdesrc-build /root/kdesrc-build
# setup developer account
RUN echo 'developer ALL=NOPASSWD: ALL' >> /etc/sudoers
USER developer
ENV HOME /home/developer
WORKDIR /home/developer/
# kde anongit url alias
RUN git config --global url."git://anongit.kde.org/".insteadOf kde: && \
    git config --global url."ssh://git@git.kde.org/".pushInsteadOf kde: && \
    git config --global url."https://git.kolab.org/diffusion/".insteadOf kolab: && \
    git config --global url."ssh://git@git.kolab.org/diffusion/".pushInsteadOf kolab: && \
    git config --global user.email "developer@example.com" && \
    git config --global user.name "Developer" && \
    git clone git://anongit.kde.org/kdesrc-build.git

VOLUME /work
VOLUME /qt


ENTRYPOINT ["/bin/bash"]
