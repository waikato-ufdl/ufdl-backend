# Ubuntu 18.04 with Python 3.7
ARG DOCKER_REGISTRY=public.aml-repo.cms.waikato.ac.nz:443/
FROM ${DOCKER_REGISTRY}ubuntu:bionic

ARG PYTHON=python3.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends git-core libglib2.0-0 libsm6 libxrender-dev libxrender1 libxext6 && \
    apt-get install -y build-essential ${PYTHON} ${PYTHON}-dev lib${PYTHON}-dev virtualenv && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /ufdl && \
    cd /ufdl && \
    git clone https://github.com/waikato-ufdl/ufdl-json-messages.git && \
    git clone https://github.com/waikato-ufdl/ufdl-backend.git && \
    cd /ufdl/ufdl-backend && \
    ./dev_init.sh -y

COPY bash.bashrc /etc/bash.bashrc

WORKDIR /
