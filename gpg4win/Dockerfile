FROM debian:wheezy

RUN apt-get update
RUN apt-get -y install build-essential automake autoconf mingw32 mingw-w64 mingw-w64-i686-dev mingw-w64-x86-64-dev nsis stow unzip texinfo imagemagick docbook-utils sharutils gettext libglib2.0-dev libgdk-pixbuf2.0-dev docbook-utils ghostscript texlive texlive-latex-extra texlive-lang-german latex-xcolor libqt4-dev-bin
RUN apt-get -y install wget
RUN mkdir /work/ && cd /work/ && wget http://files.gpg4win.org/gpg4win-2.2.5.tar.bz2 && tar xaf gpg4win-2.2.5.tar.bz2
RUN cd /work/gpg4win-2.2.5/packages && sh download.sh
# RUN cd /work/gpg4win-2.2.5/ && ./autogen.sh --build-w32
#Make fails while building the installer with nsis
# RUN cd /work/gpg4win-2.2.5/ && make
#Building only the vanilla installer works
# RUN cd /work/gpg4win-2.2.5/src && make gpg4win-vanilla-2.2.5.exe
