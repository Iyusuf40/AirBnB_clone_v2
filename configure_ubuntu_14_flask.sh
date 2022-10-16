#!/bin/bash
# configures an ubuntu server with python3.4.3 installed to
# install and use flask
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo apt-get install curl
curl -O https://bootstrap.pypa.io/pip/3.4/get-pip.py
sudo python3 get-pip.py
sudo pip3 install -U setuptools
pip install jinja2==2.*
pip install flask==0.*
