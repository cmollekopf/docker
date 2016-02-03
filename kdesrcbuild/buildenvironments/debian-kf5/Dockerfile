FROM debian:sid

RUN echo "deb-src http://httpredir.debian.org/debian/ sid main non-free contrib" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y dist-upgrade
RUN apt-get -y install git bzr
RUN apt-get -y install libxml-perl libjson-perl
RUN apt-get -y install libsm-dev libpcre3-dev
RUN apt-get -y install xsltproc
RUN apt-get -y install sudo

RUN apt-get -y install qtbase5-dev qtbase5-dev-tools cmake doxygen libsqlite3-de libsqlite3-dev

#kdepimlibs
RUN apt-get -y install libgpgme11-dev libboost-graph-dev libsasl2-dev libqjson-dev libical-dev libldap2-dev

#baloo
RUN apt-get -y install libxapian-dev

#libkolabxml
RUN apt-get -y install libboost-thread-dev libboost-system-dev xsdcxx libxerces-c-dev libcurl4-openssl-dev

#zanshin
RUN apt-get -y install libboost-dev libboost-regex-dev

RUN apt-get install -y qtscript5-dev gettext libqt5x11extras5-dev libxcb-keysyms1-dev libxrender-dev

RUN apt-get install -y libxslt-dev docbook-xml docbook-xsl libxml2-utils
RUN apt-get install -y libpolkit-agent-1-dev qttools5-dev

RUN apt-get install -y libqt5svg5-dev libudev-dev libgcrypt11-dev
RUN apt-get install -y qtdeclarative5-dev libepoxy-dev
RUN apt-get install -y libqt5webkit5-dev libssl-dev libpng-dev libjpeg-dev libgif-dev

RUN apt-get install -y libxcursor-dev ttf-oxygen-font-family qtbase5-private-dev libqt5xmlpatterns5-dev
RUN apt-get install -y libvlc-dev libvlccore-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev network-manager-dev libnm-dev 
RUN apt-get install -y libattr1-dev
RUN apt-get install -y qt4-dev-tools libqt4-dev libdmtx-dev libqrencode-dev

RUN apt-get install -y libboost-program-options-dev qttools5-dev-tools liblmdb-dev

#for tests
RUN apt-get install -y gpgsm xvfb oxygen-icon-theme dbus-x11

#for sink
Run apt-get install -y clang libreadline-dev libgit2-dev

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

ENV DISPLAY :0
ENV LANG "de_DE.Utf-8"

ENTRYPOINT ["/bin/bash"]
