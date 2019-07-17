FROM python:3.7
ENV SHELL /bin/bash

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  apt-utils 2>&1

RUN apt-get -y install git procps lsb-release
RUN apt-get install -y libicu[0-9][0-9]

RUN apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND dialog

RUN mkdir /workspace
WORKDIR /workspace

## Virtualenv ##
RUN pip install virtualenv
ENV VIRTUAL_ENV=/workspace/venv
RUN python -m virtualenv --python=/usr/local/bin/python $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
##

COPY requirements.txt /workspace/
RUN pip install -r requirements.txt
COPY requirements-dev.txt /workspace/
RUN pip install -r requirements-dev.txt