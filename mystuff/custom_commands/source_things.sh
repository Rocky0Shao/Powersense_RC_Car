source /home/rocky/Powersense_RC_Car/venv/bin/activate
export PYTHONPATH="$(python3 -c 'import site; print(site.getsitepackages()[0])'):$PYTHONPATH"
source /opt/ros/jazzy/setup.bash
source /home/rocky/Powersense_RC_Car/install/setup.bash
ros2 run camera_realsense camera_interface_node