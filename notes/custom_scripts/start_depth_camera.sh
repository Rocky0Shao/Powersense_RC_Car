source /opt/ros/jazzy/setup.bash
source install/setup.bash
export PYTHONPATH=/home/rocky/Powersense_RC_Car/myenv/lib/python3.12/site-packages:$PYTHONPATH
ros2 run camera_realsense camera_interface_node
