#!/bin/bash
sudo apt-get update
sudo apt-get -y install python-setuptools
sudo apt-get -y install python-pip
sudo pip install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz
