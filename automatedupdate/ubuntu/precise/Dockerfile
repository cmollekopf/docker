From ubuntu:12.04

RUN apt-get update && apt-get -y install \
    wget

#Add repo key
RUN wget http://obs.kolabsys.com/repositories/Kontact:/4.13:/Development/Ubuntu_12.04/Release.key && apt-key add Release.key

RUN echo "deb http://obs.kolabsys.com/repositories/Kontact:/4.13:/Development/Ubuntu_12.04/ /" > /etc/apt/sources.list.d/kolab-obs-git.list
RUN echo "Package: *\nPin: origin obs.kolabsys.com\nPin-Priority: 501"  > /etc/apt/preferences.d/obs-kolab 

# Some Environment Variables
ENV    DEBIAN_FRONTEND noninteractive

RUN echo "mysql-server-5.5 mysql-server-5.5/start_on_boot boolean true" | debconf-set-selections &&\
    echo "mysql-server-5.5 mysql-server-5.5/nis_warning note"| debconf-set-selections &&\
    echo "mysql-server-5.5 mysql-server-5.5/really_downgrade boolean false"| debconf-set-selections &&\
    echo "mysql-server-5.5 mysql-server-5.5/postrm_remove_databases boolean false"| debconf-set-selections &&\
    echo "console-setup console-setup/codeset47 select" | debconf-set-selections  && \
    echo "console-setup console-setup/codesetcode string Lat15" | debconf-set-selections  && \
    echo "console-setup console-setup/fontface47 select VGA" | debconf-set-selections  && \
    echo "console-setup console-setup/fontsize-text47 select 16" | debconf-set-selections  && \
    echo "keyboard-configuration console-setup/ask_detect boolean false" | debconf-set-selections  && \
    echo "console-setup console-setup/store_defaults_in_debconf_db boolean true" | debconf-set-selections  && \
    echo "console-setup console-setup/charmap47 select UTF-8" | debconf-set-selections  && \
    echo "console-setup console-setup/fontsize-fb47 select 16" | debconf-set-selections  && \
    echo "keyboard-configuration console-setup/detected note" | debconf-set-selections  && \
    echo "console-setup console-setup/fontsize string 16" | debconf-set-selections  && \
  apt-get update && apt-get -y install \
    acl \
    dbus-x11 \
    git \
    kontact \
    kwalletcli \
    mysql-server \
    sudo \
    python-gobject \
    python-dbus \
    xserver-xorg-video-intel

RUN echo 'developer ALL=NOPASSWD: ALL' >> /etc/sudoers

RUN useradd -d /home/developer -m developer
RUN mkdir /work
RUN chown -R developer:developer /work
USER developer

RUN git config --global url."git://anongit.kde.org/".insteadOf kde: && \
    git config --global url."ssh://git@git.kde.org/".pushInsteadOf kde: && \
    git config --global url."https://git.kolab.org/diffusion/".insteadOf kolab: && \
    git config --global url."ssh://git@git.kolab.org/diffusion/".pushInsteadOf kolab: && \
    git config --global url."https://github.com/".insteadOf github: && \
    git config --global url."git@github.com:".pushInsteadOf github: && \
    git config --global user.email "developer@example.com" && \
    git config --global user.name "Developer"

ENV HOME /home/developer
WORKDIR /home/developer/
ENV DISPLAY :0
ENV LANG "de_DE.Utf-8"

VOLUME /work
ENTRYPOINT ["/bin/bash"]
