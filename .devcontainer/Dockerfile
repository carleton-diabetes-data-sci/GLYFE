FROM nvcr.io/nvidia/pytorch:24.04-py3
RUN apt-get -y update
RUN apt-get -y install sudo
RUN wget -O- http://neuro.debian.net/lists/jammy.us-nh.libre | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-key adv --recv-keys --keyserver hkps://keyserver.ubuntu.com 0xA5D32F012649A5A9
RUN apt-get -y update
RUN apt-get -y install git-annex
RUN apt-get -y install lsb-release
RUN pip install matplotlib
RUN pip install patsy
RUN pip install setuptools
RUN pip install statsmodels
RUN pip install datalad

# create a csuser for use rather than root
RUN useradd -ms /bin/bash csuser



# last thing because other commands need root
USER csuser
