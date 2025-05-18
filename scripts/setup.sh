#!/usr/bin/env bash
# EnviroPulse setup script
# Installs dependencies and prepares environment

set -e

# Update package list and install OS dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv cifs-utils git

# Create project directories
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Create and activate Python venv
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Upgrade pip and install Python libs
pip install --upgrade pip
pip install \
  pyyaml \
  schedule \
  flask \
  matplotlib \
  adafruit-circuitpython-bmp3xx \
  adafruit-circuitpython-sht31d \
  adafruit-circuitpython-gps \
  Adafruit-ADS1x15 \
  RPi.GPIO

# Create data directory
mkdir -p data

echo "Setup complete. Activate the venv with 'source venv/bin/activate' and run 'python src/main.py'"

