#!/usr/bin/env bash
set -e

source /home/rocky/Powersense_RC_Car/venv/bin/activate
export PYTHONPATH="$(python3 -c 'import site; print(site.getsitepackages()[0])'):$PYTHONPATH"
source /opt/ros/jazzy/setup.bash
source /home/rocky/Powersense_RC_Car/install/setup.bash

ros2 launch rplidar_a2m8 rplidar.launch.py
