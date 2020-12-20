#! /bin/bash

sudo apt update -y
sudo apt install -y python3-pip traceroute

sudo pip3 install -r /tmp/requirements.txt

sudo pip3 install -e /home/vagrant/pyns2

sudo cp /home/vagrant/pyns2/bin/pyns2 /usr/local/bin/pyns2

# bpf
#sudo apt install -y bison build-essential cmake flex git libedit-dev \
#  libllvm7 llvm-7-dev libclang-7-dev python zlib1g-dev libelf-dev \
#  python3-distutils
#
#git clone https://github.com/iovisor/bcc.git
#mkdir bcc/build; cd bcc/build
#cmake ..
#make
#sudo make install
#cmake -DPYTHON_CMD=python3 .. # build python3 binding
#pushd src/python/
#make
#sudo make install
#popd
