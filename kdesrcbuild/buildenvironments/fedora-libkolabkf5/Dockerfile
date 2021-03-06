FROM fedora:22

RUN yum -y update
#System deps
RUN yum -y install sudo yum-utils
RUN yum -y install gcc-c++ git doxygen cmake bzr vim tar

#kdesrcbuild deps
RUN yum -y install sudo perl-libwww-perl perl-JSON perl-XML-Parser

#Clang + Ninja
RUN yum -y install ninja-build clang

#Test debugging
RUN yum -y install gdb

#Frameworks
RUN yum -y install qt5-qtscript-devel qt5-qttools-devel qt5-qtsvg-devel qt5-qtx11extras-devel xcb-util-keysyms-devel qt5-qttools-static polkit-devel qt5-qtdeclarative-devel libepoxy-devel qt5-qtwebkit-devel qt5-qtxmlpatterns-devel

#icecream
RUN yum -y install icecream

#autotools
RUN yum -y install autoconf libtool

#libkolabxml
RUN yum -y install xerces-c-devel curl-devel boost-system xsd

#libkolab
RUN yum -y install kdepimlibs-devel

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
