FROM python:3.8

ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
    && apt-get upgrade -y

RUN curl -sL https://deb.nodesource.com/setup_12.x |bash - \
    && apt-get install -y --no-install-recommends \
    wget \
    git \
    vim \
    curl \
    nodejs \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /usr/local/src/* \
        /tmp/*

COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

WORKDIR /tmp/working


RUN pip3 install --upgrade --no-cache-dir \
    'jupyterlab~=3.0' \
    'jupyterlab-kite>=2.0.2' \
    jupyterlab_code_formatter \
    yapf \
    && rm -rf ~/.cache/pip \
    && jupyter labextension install \
        @hokyjack/jupyterlab-monokai-plus \
        @ryantam626/jupyterlab_code_formatter \
        @jupyterlab/toc \
    && jupyter serverextension enable --py jupyterlab_code_formatter

RUN wget https://linux.kite.com/dls/linux/current && \
    chmod 777 current && \
    sed -i 's/"--no-launch"//g' current > /dev/null && \
    ./current --install ./kite-installer
