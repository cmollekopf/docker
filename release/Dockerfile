FROM debian:jessie

RUN echo 'Acquire::http { Proxy "http://172.16.0.1:3142" }' >  /etc/apt/apt.conf.d/01proxy

RUN echo "deb http://httpredir.debian.org/debian/ sid main" > /etc/apt/sources.list
RUN echo "deb-src http://httpredir.debian.org/debian/ sid main" >> /etc/apt/sources.list
RUN apt-get update && apt-get -y install \
	bash sudo devscripts \
	vim git \
	ipython3 python3 python3-debian python3-git \
	osc

RUN useradd -d /home/developer -m developer
RUN mkdir /work
RUN chown developer /work

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
    git config --global url."https://github.com/".insteadOf github: && \
    git config --global url."git@github.com:".pushInsteadOf github: && \
    git config --global user.email "developer@example.com" && \
    git config --global user.name "Developer"

VOLUME /work

ENV DISPLAY :0
ENV LANG "de_DE.UTF-8"

RUN mkdir -p /home/developer/.local/lib/python3.5/dist-packages
RUN chown developer /home/developer/.local/lib/python3.5/dist-packages
RUN ln -s /home/developer/release /home/developer/.local/lib/python3.5/dist-packages/

ENTRYPOINT ["/bin/bash"]
