FROM fedora:23

RUN dnf -y update

RUN dnf -y install gcc-c++ git doxygen cmake bzr vim tar ninja-build clang

#kdesrcbuild deps
RUN dnf -y install sudo perl-libwww-perl perl-JSON perl-JSON-PP perl-XML-Parser

#PIM deps
RUN dnf -y install boost-devel sqlite prison-devel openldap-devel libical-devel libical-devel gpgme-devel

#Sink deps
RUN dnf -y install extra-cmake-modules qt5-qtbase-devel libgit2-devel lmdb-devel readline-devel
RUN dnf -y install xterm

#Test debugging
RUN dnf -y install gdb xterm perf

#Frameworks
RUN dnf -y install qt5-qtscript-devel qt5-qttools-devel qt5-qtsvg-devel qt5-qtx11extras-devel xcb-util-keysyms-devel qt5-qttools-static polkit-devel qt5-qtdeclarative-devel libepoxy-devel qt5-qtwebkit-devel qt5-qtxmlpatterns-devel

#Kube
RUN dnf -y install kf5-kpackage-devel libcurl-devel

#kmime
RUN dnf -y install kf5-ki18n-devel kf5-kcodecs-devel
#For KDocTools
RUN dnf -y install kf5-karchive-devel
#For KConfigWidgets
RUN dnf -y install kf5-kdoctools-devel kf5-kwidgetsaddons-devel kf5-kguiaddons-devel
#For KAuth
RUN dnf -y install kf5-kcoreaddons-devel
#For KConfigWidgets
RUN dnf -y install kf5-kconfig-devel kf5-kauth-devel
#For KIconThemes
RUN dnf -y install kf5-kitemviews-devel kf5-kconfigwidgets-devel
#For libotp
RUN dnf -y install kf5-kiconthemes-devel

#KDocTools
RUN sudo dnf -y install libxml2-devel libxslt-devel docbook-style-xsl

# Support
RUN dnf -y install icecream

# Headless UI tests
RUN dnf -y install xorg-x11-server-Xvfb

RUN dnf -y install qt5-qtgraphicaleffects qt5-qtquickcontrols

RUN dnf -y install cyrus-imapd cyrus-sasl cyrus-sasl-plain
RUN dnf -y install gnupg2-smime

#For kimap
RUN dnf -y install kf5-kio-devel

RUN dnf -y install qt5-qtwebengine-devel

RUN dnf -y install valgrind kcachegrind dbus-x11

#for GpgME
RUN dnf -y install automake autoconf libassuan-devel texinfo texlive-epstopdf

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

#Setup cyrus imap
RUN sudo usermod -p `perl -e "print crypt("admin","Q4")"` cyrus
RUN sudo useradd -p `perl -e "print crypt("doe","Q4")"` doe
RUN sudo saslauthd -a pam && sudo /usr/lib/cyrus-imapd/cyrus-master -d && sudo echo "cm user.doe" | cyradm --auth PLAIN -u cyrus -w admin localhost

#For KCacheGrind
RUN sudo dbus-uuidgen --ensure
#Disable abrt
RUN sudo systemctl disable abrt-ccpp

VOLUME /work
VOLUME /qt

ENTRYPOINT ["/bin/bash"]
