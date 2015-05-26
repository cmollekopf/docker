FROM fedora:21

# Add RPM Fusion
RUN rpm -ivh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm

# Install dependencies
#---------------------------
RUN yum -y install gcc-c++ git doxygen cmake bzr vim tar && \
    yum -y install dialog perl-libwww-perl perl-JSON perl-XML-Parser \
                    qt4-devel && \
    yum install -y \
                    libXrender-devel xcb-util-keysyms-devel \
                    zlib-devel \
                    libxslt-devel docbook-style-xsl \
                    systemd-devel \
                    libepoxy-devel\
                    boost-devel \
                    libSM-devel pcre-devel qca-ossl openssl-devel \
                    giflib-devel libjpeg-turbo-devel libpng-devel \
                    libXcursor-devel oxygen-fonts-devel \
                    polkit-devel \
                    vlc-devel \
                    gstreamer-devel gstreamer-plugins-bad-free-devel gstreamer1-plugins-bad-free-devel gstreamer1-plugins-base-devel \
                                NetworkManager-devel NetworkManager-glib-devel && \
    yum install -y \
                    libattr-devel \
                    ModemManager-devel \
                    xcb-util-image-devel \
                    xorg-x11-xkb-utils-devel \
                    libpwquality-devel \
                    xorg-x11-drv-synaptics-devel xorg-x11-server-devel \
                    gtkmm24-devel gtkmm30-devel \
                    xapian-core-devel \
                    libepoxy-devel \
                    libmms-devel \
                    fontforge-devel \
                    exiv2-devel \
                    sane-backends-devel && \
    yum install -y \ 
                    lcms2-devel \
                    hunspell-devel \
                    glui-devel \
                    eigen3-devel \
                    grantlee-devel \
                    qtsinglecoreapplication-devel \
                    libarchive-devel \
                    alsa-lib alsa-lib-devel \
                    openal-soft-devel libsndfile-devel \
                    gmp-devel \
                    cups-devel \
                    qca2-devel qca-ossl qca-gnupg qca-pkcs11 && \
    yum install -y \ 
                    libdmtx-devel qrencode-devel \
                    libical-devel \
                    cyrus-sasl-devel \
                    openldap-devel \
                    gpgme-devel && \
    useradd -d /home/kdedev -m kdedev && \
    mkdir /work /qt && \
    chown kdedev /work /qt

RUN yum install -y automoc phonon-devel qtwebkit-devel attica-devel dbusmenu-qt-devel strigi-devel qjson-devel libcurl-devel xsd xerces

# some symlinks in /root to handle sudo ./kdesrc-build
RUN ln -s /home/kdedev/.kdesrc-buildrc /root/.kdesrc-buildrc && \
    ln -s /home/kdedev/kdesrc-build /root/kdesrc-build
# setup kdedev account
RUN yum install -y sudo && echo 'kdedev ALL=NOPASSWD: ALL' >> /etc/sudoers
USER kdedev
ENV HOME /home/kdedev
WORKDIR /home/kdedev/
# kde anongit url alias
RUN git config --global url."git://anongit.kde.org/".insteadOf kde: && \
    git config --global url."ssh://git@git.kde.org/".pushInsteadOf kde: && \
    git clone git://anongit.kde.org/kdesrc-build.git 

VOLUME /work
VOLUME /qt

ENTRYPOINT ["/bin/bash"]
