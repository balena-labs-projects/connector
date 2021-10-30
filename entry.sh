#!/bin/bash
set -e

# Run balena base image entrypoint script
/usr/bin/entry.sh echo ""

echo "balenaBlocks connector version: $(<VERSION)"

hn=$BALENA_DEVICE_UUID
hp=$(echo $hn | cut -c1-7)
echo 'Changing hostname to '$hp
hostname $hp

if [ -z "$1" ]
  then
    echo "Generating config"
    python3 ./autowire.py
    exec ./telegraf --config ./telegraf.conf
    exit
fi

# If command starts with an option, prepend telegraf to it
if [[ "${1#-}" != "$1" ]]; then
  set -- ./telegraf "$@"
fi

exec "$@"
