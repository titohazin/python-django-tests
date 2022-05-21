FROM python:3.10.4-slim

# for Git and Git Lens extensions support
RUN apt update && apt install -y --no-install-recommends git zsh curl wget fonts-powerline gnupg pinentry-tty

# for SonarLint extension support
RUN apt install -y --no-install-recommends default-jre
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Python Package Manager
RUN pip install pdm>=1.15.0

# Add non-root user
RUN useradd -ms /bin/bash python
USER python

RUN mkdir -p /home/python/app
WORKDIR /home/python/app

# Container ZSH configurations (with powerlevel10k theme or -- -t theme_name, -p plugin_name)
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p git-flow \
    -p gpg-agent \
    -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-history-substring-search \
    -a 'export TERM=xterm-256color'

RUN echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc
RUN echo 'HISTFILE=/home/python/zsh/.zsh_history' >> ~/.zshrc

# PDM (Python Package Manager) configs
ENV PATH="/home/python/app/__pypackages__/3.10/bin:${PATH}"
RUN echo 'eval "$(pdm --pep582)"' >> ~/.bashrc
RUN echo 'eval "$(pdm --pep582)"' >> ~/.zshrc

ENV PYTHONPATH=${PYTHONPATH}/home/python/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1