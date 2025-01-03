FROM nvcr.io/nvidia/pytorch:24.04-py3

RUN wget -O- http://neuro.debian.net/lists/jammy.us-nh.libre | tee /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-key adv --recv-keys --keyserver hkps://keyserver.ubuntu.com 0xA5D32F012649A5A9
RUN apt-get -y update

RUN apt-get -y install zsh 

#COPY conda-diabetes.yml /tmp/conda-diabetes.yml

RUN apt-get -y install sudo
RUN apt-get -y install lsb-release
RUN apt-get -y install datalad
RUN apt-get -y install tig

RUN pip install matplotlib
RUN pip install patsy
RUN pip install setuptools
RUN pip install statsmodels
RUN pip install datalad

# # create a csuser for use rather than root
RUN useradd -ms /bin/bash vscode

# last thing because other commands need root
USER vscode
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Make RUN commands use `bash --login`:
SHELL ["/bin/bash", "--login", "-c"]

# Set up zsh prompt
# Varying RobbyRussell oh-my-zsh theme
# https://github.com/ohmyzsh/ohmyzsh/blob/master/themes/robbyrussell.zsh-theme
RUN echo 'PROMPT="%(?:%{$fg_bold[green]%}%1{➜%} :%{$fg_bold[red]%}%1{➜%} ) %{$fg[cyan]%}%d%{$reset_color%}"' >> ~/.zshrc
RUN echo 'PROMPT+='\'' $(git_prompt_info)'\' >> ~/.zshrc
RUN echo 'ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}(%{$fg[red]%}"' >> ~/.zshrc