FROM fedora:25

RUN dnf -y install 'dnf-command(copr)'
RUN dnf -y copr enable @kdesig/qt-5.9
RUN dnf -y update

RUN dnf -y install gcc-c++ git doxygen cmake bzr vim tar ninja-build clang

#kdesrcbuild deps
RUN dnf -y install sudo perl-libwww-perl perl-JSON perl-JSON-PP perl-XML-Parser

#Sink deps
RUN dnf -y install extra-cmake-modules qt5-qtbase-devel libgit2-devel lmdb-devel readline-devel libcurl-devel

#Test and debugging
RUN dnf -y install gdb xterm perf valgrind

#kf5-mime
RUN dnf -y install cyrus-sasl-devel

#Stuff for kube
RUN dnf -y install qt5-qtquickcontrols qt5-qtquickcontrols2-devel qt5-qtwebengine-devel
RUN dnf -y install kf5-kpackage-devel kf5-ki18n-devel kf5-kcodecs-devel kf5-kcontacts-devel kf5-kmime-devel qgpgme-devel

# Support
RUN dnf -y install icecream

# Headless UI tests
RUN dnf -y install xorg-x11-server-Xvfb

# Imap tests
RUN dnf -y install cyrus-imapd cyrus-sasl cyrus-sasl-plain gnupg2-smime

#KCachegrind needs dbus =(
RUN dnf -y install kcachegrind dbus-x11


RUN sed -i 's/5.9.0/5.8.0/g' /usr/lib64/cmake/Qt5WebEngineWidgets/Qt5WebEngineWidgetsConfig.cmake
RUN sed -i 's/5.9.0/5.8.0/g' /usr/lib64/cmake/Qt5WebEngineCore/Qt5WebEngineCoreConfig.cmake
RUN sed -i 's/5.9.0/5.8.0/g' /usr/lib64/cmake/Qt5WebEngine/Qt5WebEngineConfig.cmake

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
RUN sudo saslauthd -a pam && sudo /usr/lib/cyrus-imapd/cyrus-master -d && sleep 1 && sudo echo "cm user.doe" | cyradm --auth PLAIN -u cyrus -w admin localhost

#For KCacheGrind
RUN sudo dbus-uuidgen --ensure

VOLUME /work
VOLUME /qt

ENTRYPOINT ["/bin/bash"]
