FROM debian:sid
VOLUME [ "/sys/fs/cgroup" ]
RUN echo 'Acquire::http { Proxy "http://172.16.0.1:3142" }' >  /etc/apt/apt.conf.d/01proxy

RUN echo "deb http://httpredir.debian.org/debian/ sid main" > /etc/apt/sources.list
RUN echo "deb-src http://httpredir.debian.org/debian/ sid main" >> /etc/apt/sources.list
RUN apt-get update && apt-get -y install \
    cmake clang git bzr libxml-perl libjson-perl sudo \
    doxygen docbook-xml docbook-xsl gettext libxml2-utils texinfo libxslt-dev xsdcxx xsltproc \
    fonts-oxygen \
    libattr1-dev \
    libcurl4-openssl-dev \
    libdmtx-dev \
    libepoxy-dev \
    libgcrypt11-dev \
    libgpgme-dev \
    libical-dev \
    libldap2-dev \
    liblmdb-dev \
    libpcre3-dev \
    libpng-dev libjpeg-dev libgif-dev \
    libpolkit-agent-1-dev \
    libreadline-dev \
    libsasl2-dev \
    libsm-dev \
    libssl1.0-dev \
    libudev-dev \
    libvlc-dev libvlccore-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev network-manager-dev libnm-dev \
    libxapian-dev \
    libxcb-keysyms1-dev libxrender-dev \
    libxcursor-dev \
    libxerces-c-dev \
    \
    gdb gpgsm xvfb oxygen-icon-theme dbus-x11 vim \
    \
    libboost-dev libboost-graph-dev libboost-thread-dev libboost-system-dev \
    libboost-regex-dev libboost-program-options-dev flex bison \
    \
    qtbase5-dev qtbase5-dev-tools qtbase5-private-dev \
    qtdeclarative5-dev qtscript5-dev qttools5-dev qttools5-dev-tools \
    libqrencode-dev \
    libsqlite3-dev libqt5svg5-dev \
    libqt5webkit5-dev qtwebengine5-dev libqt5webenginewidgets5 \
    libqt5x11extras5-dev libqt5xmlpatterns5-dev libqjson-dev


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
