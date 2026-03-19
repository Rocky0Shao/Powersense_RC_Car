# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research robotics project benchmarking energy-to-performance trade-offs for autonomous navigation. It uses ROS 2 Jazzy on a Jetson Nano with an Intel RealSense D455, RPLidar A2M8, and INA3221/INA260 power monitors. The core metric is Energy-per-Meter (EpM = ∫P(t)dt / distance).

## Environment Setup (Required Order)

```bash
source /home/rocky/Powersense_RC_Car/venv/bin/activate
export PYTHONPATH="$(python3 -c 'import site; print(site.getsitepackages()[0])'):$PYTHONPATH"
source /opt/ros/jazzy/setup.bash
source /home/rocky/Powersense_RC_Car/install/setup.bash
```

## Build Commands

```bash
# Build individual packages
colcon build --packages-select rplidar_a2m8
colcon build --packages-select camera_realsense
colcon build --packages-select power_monitor
colcon build --packages-select custom_msgs

# Build all
colcon build
```

## Running Nodes

```bash
ros2 launch rplidar_a2m8 rplidar.launch.py
ros2 run camera_realsense camera_interface_node
ros2 run power_monitor bridge_node
```

## Hardware Firmware (ESP32 / PlatformIO)

```bash
cd hardware_testing/Power_Monitor_INA3221/
pio build -e esp-wrover-kit
pio upload -e esp-wrover-kit --upload-port /dev/esp32
pio monitor --port /dev/esp32
```

## Architecture

### ROS 2 Packages (`src/`)

- **`rplidar_a2m8`** — Wraps the `rplidar-roboticia` Python driver; publishes `sensor_msgs/LaserScan` on `/scan`. Configurable port, baudrate, scan_mode, and inversion via launch parameters.
- **`camera_realsense`** — Uses `pyrealsense2` to stream RealSense D455 at 640×480/30 Hz; publishes `sensor_msgs/Image` (color) and `sensor_msgs/PointCloud2` (aligned depth).
- **`power_monitor`** — Serial bridge that reads CSV lines from the ESP32 (`voltage,current,power`) at 115200 baud and publishes on ROS topics using the custom `Power_Consumption` message.
- **`custom_msgs`** — CMake package defining `Power_Consumption.msg` (`float64 voltage, current, power`). Must be built before `power_monitor`.

### ESP32 Firmware (`hardware_testing/Power_Monitor_INA3221/`)

Arduino sketch (C++) running on ESP32 WROVER Kit. Reads 3-channel INA3221 sensor at 10 Hz and outputs CSV over Serial at 115200 baud. The ROS `power_monitor` node consumes this stream.

### Data Flow

```
ESP32 (INA3221) --serial CSV--> power_monitor/serial_bridge.py --ROS topic--> /power
RPLidar A2M8 --USB--> rplidar_interface_node.py --> /scan (LaserScan)
RealSense D455 --USB3--> camera_interface_node.py --> /color/image_raw, /pointcloud
```

### Custom Messages

`custom_msgs` must be built first since `power_monitor` depends on it. The `Power_Consumption.msg` is in `custom_msgs/msg/`.

## Key Files

- `src/power_monitor/power_monitor/serial_bridge.py` — ROS node reading serial from ESP32
- `src/rplidar_a2m8/launch/rplidar.launch.py` — Configurable launch file
- `hardware_testing/Power_Monitor_INA3221/src/main.cpp` — ESP32 firmware
- `mystuff/custom_commands/start_rplidar.sh` — Helper script for RPLidar startup
