#!/bin/sh

outfile="/tmp/telegraf.tar.gz"
download_base="https://dl.influxdata.com/telegraf/releases/"
case $1 in
   aarch64) package_file="telegraf-1.20.2_linux_arm64.tar.gz"
       ;;
    *) package_file="telegraf-1.20.2_linux_armhf.tar.gz"
esac
wget -O "${outfile}" "${download_base}${package_file}"

tar -xvf /tmp/telegraf.tar.gz
cp ./telegraf-1.20.2/usr/bin/telegraf ./
rm -rf ./telegraf-1.20.2
