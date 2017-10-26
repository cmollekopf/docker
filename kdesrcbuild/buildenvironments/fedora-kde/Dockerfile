FROM fedora:22

#System deps
RUN dnf -y erase vim-minimal
RUN dnf -y install sudo vim
RUN dnf -y install gcc-c++ git doxygen cmake bzr tar
RUN dnf -y install qt4-devel automoc phonon-devel qtwebkit-devel attica-devel dbusmenu-qt-devel strigi-devel qjson-devel libcurl-devel xsd xerces-c xapian-core-devel kdelibs-devel
#kdesrcbuild deps
RUN dnf -y install sudo perl-libwww-perl perl-JSON perl-JSON-PP perl-XML-Parser perl-IPC-Cmd
#up until kdelibs
RUN dnf -y install dnf-plugins-core
RUN dnf builddep -y kdelibs
#PIM deps
RUN dnf -y install boost-devel sqlite prison-devel openldap-devel libical-devel libical-devel gpgme-devel
RUN dnf -y install dbus-x11

#Clang + Ninja
RUN dnf -y install ninja-build clang

#Sink deps
RUN dnf -y install extra-cmake-modules qt5-qtbase-devel libgit2-devel lmdb-devel readline-devel
RUN dnf -y install xterm

#Test debugging
RUN dnf -y install gdb perf

#Frameworks
RUN dnf -y install qt5-qtscript-devel qt5-qttools-devel qt5-qtsvg-devel qt5-qtx11extras-devel xcb-util-keysyms-devel qt5-qttools-static polkit-devel qt5-qtdeclarative-devel libepoxy-devel qt5-qtwebkit-devel qt5-qtxmlpatterns-devel

#Kube
RUN dnf -y install kf5-kpackage-devel

#kmime
RUN dnf -y install kf5-ki18n-devel kf5-kcodecs-devel

#icecream
RUN dnf -y install icecream

#autotools
RUN dnf -y install autoconf libtool

#pep
RUN dnf -y install sqlite-devel

#libkolabxml
RUN dnf -y install xerces-c-devel

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
