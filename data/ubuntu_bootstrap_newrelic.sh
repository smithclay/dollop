#!/bin/bash
sudo echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list
sudo wget -O- https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install newrelic-sysmond
sudo apt-get -y install python-setuptools
sudo apt-get -y install python-pip
sudo pip install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz
