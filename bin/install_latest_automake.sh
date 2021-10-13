#! /usr/bin/env bash

GNU_AUTOMAKE_MIRROR="https://mirror.us-midwest-1.nexcess.net/gnu/automake/automake-1.16.3.tar.gz"

wget ${GNU_AUTOMAKE_MIRROR} -O automake.tar.gz
tar -xf automake.tar.gz
cd automake-1.16.3
./configure
sudo make install
rm -rf automake-1.16.3 automake.tar.gz
