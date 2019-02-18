#!/bin/bash

locale-gen en_US en_US.UTF-8 pt_BR.UTF-8
dpkg-reconfigure locales

apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list

apt-get update -qq
apt-get install apparmor apt-transport-https ca-certificates linux-image-extra-$(uname -r) -y

apt-get install docker-engine -y
service docker start

groupadd docker
usermod -aG docker ubuntu
