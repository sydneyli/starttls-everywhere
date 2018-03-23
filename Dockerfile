FROM ubuntu:16.04
MAINTAINER Sydney Li

WORKDIR /opt/starttls-everywhere

ENV DEBIAN_FRONTEND noninteractive
ENV NAME valid-example-recipient

# add-apt-repository is not in base image, so we need to install it.
RUN apt-get update
RUN apt-get install -y software-properties-common

# Install dependencies
RUN apt-get install -y postfix dnsmasq mutt vim git

# Install certbot (with postfix branch)
RUN git clone https://github.com/sydneyli/certbot
RUN cd certbot && git checkout postfix
RUN ./certbot/certbot-auto -n --os-packages-only
RUN cd certbot && ./tools/venv.sh

# Vagrant-shared has certs and initial config files.
ADD vagrant-shared/ .

# Install the policy API
ADD policylist/ starttls-policy/policylist/
ADD setup.cfg starttls-policy/setup.cfg
ADD setup.py starttls-policy/setup.py

RUN apt-get -y install netcat dnsutils telnet

# Adding testing scripts
ADD tests tests

# Expose SMTP and SMTP submission ports.
EXPOSE 25 587

# ENTRYPOINT ["/bin/bash"]
