FROM tensorflow/tensorflow:latest-gpu
RUN apt-get -y update
RUN apt-get -y install git
RUN pip install matplotlib
RUN pip install pandas
RUN pip install scikit-learn
# # create a csuser for use rather than root
RUN useradd -ms /bin/bash csuser
USER csuser
