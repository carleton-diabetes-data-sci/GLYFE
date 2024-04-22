FROM ubuntu:latest
#FROM pytorch/pytorch:latest
#RUN apt-get -y update
#RUN apt-get -y install curl
#RUN apt-get -y install gpg
#RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
#&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
#  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
#  tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
RUN apt-get -y update
#RUN apt-get install -y nvidia-container-toolkit
RUN apt-get -y install git
RUN apt-get -y install git-annex
RUN apt-get -y install pip
RUN pip install matplotlib
RUN pip install pandas
RUN pip install scikit-learn
RUN pip install patsy
RUN pip install setuptools
RUN pip install statsmodels
RUN pip install datalad
RUN apt-get -y install file
# # create a csuser for use rather than root
RUN useradd -ms /bin/bash csuser
USER csuser
