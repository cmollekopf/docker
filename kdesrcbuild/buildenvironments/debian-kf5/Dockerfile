FROM debian:sid

RUN echo "deb http://httpredir.debian.org/debian/ sid main" > /etc/apt/sources.list
RUN echo "deb-src http://httpredir.debian.org/debian/ sid main" >> /etc/apt/sources.list
RUN apt-get update && apt-get -y install \
    git bzr libxml-perl libjson-perl libsm-dev libpcre3-dev xsltproc sudo \
    qtbase5-dev qtbase5-dev-tools cmake doxygen libsqlite3-dev \
    libgpgme11-dev libboost-graph-dev libsasl2-dev libqjson-dev libical-dev libldap2-dev \
    libxapian-dev \
    libboost-thread-dev libboost-system-dev xsdcxx libxerces-c-dev libcurl4-openssl-dev \
    libboost-dev libboost-regex-dev \
    qtscript5-dev gettext libqt5x11extras5-dev libxcb-keysyms1-dev libxrender-dev \
    libxslt-dev docbook-xml docbook-xsl libxml2-utils \
    libpolkit-agent-1-dev qttools5-dev \
    libqt5svg5-dev libudev-dev libgcrypt11-dev \
    qtdeclarative5-dev libepoxy-dev \
    libqt5webkit5-dev libssl-dev libpng-dev libjpeg-dev libgif-dev \
    libxcursor-dev ttf-oxygen-font-family qtbase5-private-dev libqt5xmlpatterns5-dev \
    libvlc-dev libvlccore-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev network-manager-dev libnm-dev \
    libattr1-dev \
    qt4-dev-tools libqt4-dev libdmtx-dev libqrencode-dev \
    libboost-program-options-dev qttools5-dev-tools liblmdb-dev

#for sink
Run apt-get install -y clang libreadline-dev libgit2-dev

#for tests
RUN apt-get install -y gpgsm xvfb oxygen-icon-theme dbus-x11 vim

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
