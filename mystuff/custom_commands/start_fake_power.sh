#!/usr/bin/env bash
set -e

# Fake Power Node Launcher
# Generates sin(t)+1 power data and optionally saves to CSV

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/rocky/Powersense_RC_Car"

# Default values
SAVE_CSV="${SAVE_CSV:-true}"
CSV_PATH="${CSV_PATH:-$HOME/power_data.csv}"
PUBLISH_RATE="${PUBLISH_RATE:-10.0}"

# Source ROS environment
source "$PROJECT_ROOT/venv/bin/activate"
export PYTHONPATH="$(python3 -c 'import site; print(site.getsitepackages()[0])'):$PYTHONPATH"
source /opt/ros/jazzy/setup.bash
source "$PROJECT_ROOT/install/setup.bash"

echo "Starting Fake Power Node..."
echo "  CSV saving: $SAVE_CSV"
echo "  CSV path: $CSV_PATH"
echo "  Publish rate: $PUBLISH_RATE Hz"
echo ""
echo "Press Ctrl+C to stop and save data."
echo ""

ros2 run power_monitor fake_power_node --ros-args \
    -p save_csv:="$SAVE_CSV" \
    -p csv_path:="$CSV_PATH" \
    -p publish_rate:="$PUBLISH_RATE"
