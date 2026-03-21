#!/usr/bin/env bash
set -e

# Plot Power Data from CSV
# Usage: ./plot_power.sh [csv_file] [--save output.png]

PROJECT_ROOT="/home/rocky/Powersense_RC_Car"
PLOT_SCRIPT="$PROJECT_ROOT/src/power_monitor/scripts/plot_power.py"

# Default CSV path
CSV_FILE="${1:-$HOME/power_data.csv}"

# Activate venv for matplotlib
source "$PROJECT_ROOT/venv/bin/activate"

if [[ ! -f "$CSV_FILE" ]]; then
    echo "Error: CSV file not found: $CSV_FILE"
    echo "Usage: $0 [csv_file] [--save output.png]"
    exit 1
fi

echo "Plotting: $CSV_FILE"

# Pass all arguments to the plot script
shift 2>/dev/null || true
python3 "$PLOT_SCRIPT" "$CSV_FILE" "$@"
