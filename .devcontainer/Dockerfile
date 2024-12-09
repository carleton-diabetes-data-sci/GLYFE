FROM nvcr.io/nvidia/pytorch:24.04-py3
#FROM mcr.microsoft.com/devcontainers/base:1-ubuntu-24.04

RUN apt-get -y update

RUN apt-get -y install zsh 

COPY conda-diabetes.yml /tmp/conda-diabetes.yml







#RUN apt-get -y install sudo
# RUN wget -O- http://neuro.debian.net/lists/jammy.us-nh.libre | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
# RUN apt-key adv --recv-keys --keyserver hkps://keyserver.ubuntu.com 0xA5D32F012649A5A9
# RUN apt-get -y update
# RUN apt-get -y install git-annex
# RUN apt-get -y install lsb-release
# RUN pip install matplotlib
# RUN pip install patsy
# RUN pip install setuptools
# RUN pip install statsmodels
# RUN pip install datalad

# # create a csuser for use rather than root
RUN useradd -ms /bin/bash vscode



# # last thing because other commands need root
USER vscode
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Make RUN commands use `bash --login`:
SHELL ["/bin/bash", "--login", "-c"]

RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh
RUN bash /tmp/miniconda.sh -b
ENV PATH="$PATH:/home/vscode/miniconda3/bin"
RUN conda init --all
RUN conda env create --name diabetes --file /tmp/conda-diabetes.yml
RUN conda clean -afy
RUN echo "conda activate diabetes" >> ~/.bashrc
RUN echo "conda activate diabetes" >> ~/.zshrc

