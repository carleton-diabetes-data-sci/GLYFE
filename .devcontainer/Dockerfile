FROM nvcr.io/nvidia/pytorch:23.11-py3
RUN apt-get -y update
RUN apt-get -y install git-annex
RUN pip install matplotlib
RUN pip install patsy
RUN pip install setuptools
RUN pip install statsmodels
RUN pip install datalad

# # create a csuser for use rather than root
RUN useradd -ms /bin/bash csuser



# last thing because other commands need root
USER csuser

