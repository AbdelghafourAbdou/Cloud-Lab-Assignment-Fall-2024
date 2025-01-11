#!/bin/bash 
sudo apt-get update
sudo apt-get install -y docker.io

sudo mkdir -p /home/user/loadGenerator && cd /home/user/loadGenerator

sudo curl -O https://cloudlabapolidockefile.s3.eu-west-3.amazonaws.com/Dockerfile
sudo curl -O https://cloudlabapolidockefile.s3.eu-west-3.amazonaws.com/locustfile.py
sudo curl -O https://cloudlabapolidockefile.s3.eu-west-3.amazonaws.com/requirements.in
sudo curl -O https://cloudlabapolidockefile.s3.eu-west-3.amazonaws.com/requirements.txt

sudo docker build -t loadgenerator .
sudo docker run --env-file /tmp/env.list -d loadgenerator