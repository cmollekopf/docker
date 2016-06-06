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
    libboost-program-options-dev qttools5-dev-tools liblmdb-dev \
    clang libreadline-dev \
    gdb gpgsm xvfb oxygen-icon-theme dbus-x11 vim

#for qt5 build
RUN apt-get -y install \
libdbus-1-dev libsrtp-dev bison build-essential gperf flex ruby python libasound2-dev libbz2-dev libcap-dev \
libcups2-dev libdrm-dev libegl1-mesa-dev libgcrypt11-dev libnss3-dev libpci-dev libpulse-dev libudev-dev \
libxtst-dev gyp ninja \
libssl-dev libxcursor-dev libxcomposite-dev libxdamage-dev libxrandr-dev libfontconfig1-dev libcap-dev libxtst-dev libpulse-dev libudev-dev libpci-dev libnss3-dev libasound2-dev libxss-dev libegl1-mesa-dev gperf \
"^libxcb.*" libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev \
libicu-dev libminizip-dev libwebp-dev libevent-dev libopus-dev libvpx-dev libsnappy-dev libjsoncpp-dev

#for akonadi
ENV    DEBIAN_FRONTEND noninteractive

RUN echo "mysql-server-5.5 mysql-server-5.5/start_on_boot boolean true" | debconf-set-selections &&\
    echo "mysql-server-5.5 mysql-server-5.5/nis_warning note"| debconf-set-selections &&\
    echo "mysql-server-5.5 mysql-server-5.5/really_downgrade boolean false"| debconf-set-selections &&\
    echo "mysql-server-5.5 mysql-server-5.5/postrm_remove_databases boolean false"| debconf-set-selections

RUN apt-get -y install \
mysql-server libmysqlclient-dev

RUN apt-get -y install \
ccache icecc

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
RUN ln -s /work/ccache /home/developer/.ccache

VOLUME /work
VOLUME /qt

ENV DISPLAY :0
ENV LANG "de_DE.Utf-8"

ENTRYPOINT ["/bin/bash"]
