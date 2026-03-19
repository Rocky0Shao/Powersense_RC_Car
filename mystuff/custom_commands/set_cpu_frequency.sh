#!/bin/bash

# Prompt the user for the frequency
read -p "Enter desired CPU frequency in GHz (e.g., 2.5): " freq

# Validate that the input is not empty
if [ -z "$freq" ]; then
    echo "Error: No frequency entered."
    exit 1
fi

# Execute the cpupower command
echo "Locking CPU frequency to ${freq}GHz..."
sudo cpupower frequency-set -d "${freq}GHz" -u "${freq}GHz"

echo "Done!"