#!/bin/sh

version="1.22.0"
outfile="/tmp/telegraf.tar.gz"
download_base="https://dl.influxdata.com/telegraf/releases/"
case $1 in
    "aarch64") package_file="telegraf-${version}_linux_arm64.tar.gz"
       ;;
    "rpi") package_file="telegraf-${veriosn}_linux_armhf.tar.gz"
       ;;
    "amd64") package_file="telegraf-${version}_static_linux_amd64.tar.gz"
       ;;
   *) echo >&2 "error: unsupported architecture ($1)"; exit 1 ;;   
esac
wget -O "${outfile}" "${download_base}${package_file}"

tar -xvf /tmp/telegraf.tar.gz
cp ./telegraf-*/usr/bin/telegraf ./
rm -rf ./telegraf-*