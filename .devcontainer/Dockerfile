# FROM lambci/lambda:build-python3.7
FROM python:3.7

RUN pip install black
RUN pip install pylint

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get -y install --no-install-recommends apt-utils 2>&1

RUN apt-get -y install git procps lsb-release

RUN apt-get install -y libicu[0-9][0-9]

RUN apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

RUN mkdir /workspace
WORKDIR /workspace

COPY requirements.txt /workspace/
RUN pip install -r requirements.txt

# COPY rmshelper /workspace/rmshelper/
# COPY app.py /workspace/