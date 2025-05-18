#!/usr/bin/env python3
"""
EnviroPulse Main Script
- Reads sensors (BMP390, SHT31, GPS, ADS1115, Davis Anemometer)
- Logs data to SQLite
- Generates daily summaries
- Serves Flask web GUI
"""
import os
import time
import math
import threading
import yaml
import sqlite3
from datetime import datetime, date, timedelta
from flask import Flask, render_template

# Placeholder imports for sensor libraries
# import board, busio, serial
# import adafruit_bmp3xx, adafruit_sht31d, adafruit_gps
# from Adafruit_ADS1x15 import ADS1115
# import RPi.GPIO as GPIO

# Load configuration
dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, '..', 'config', 'config.yaml')
with open(config_path) as f:
    cfg = yaml.safe_load(f)

app = Flask(__name__, template_folder=os.path.join(dir_path, '..', 'web', 'templates'))

def collect_data():
    """Collect a single data reading and write to database"""
    # TODO: read sensors, calculate metrics, insert into DB
    pass


def generate_summary():
    """Generate daily plots and summary statistics"""
    # TODO: query DB, create plots, write summary.txt
    pass


def run_scheduler():
    """Schedule periodic data collection and daily summary"""
    import schedule
    schedule.every(cfg['sample_interval_sec']).seconds.do(collect_data)
    schedule.every().day.at(cfg['daily_summary_time']).do(generate_summary)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def index():
    # TODO: Fetch latest data and summary from files
    return render_template('index.html', data=None, stats=None)

if __name__ == '__main__':
    # TODO: call init_db(), start scheduler thread
    app.run(host=cfg['flask']['host'], port=cfg['flask']['port'])
```
Save and exit (Ctrl+O, Enter, Ctrl+X).

---

### Step 2: Populate `config/config.yaml`
Create the configuration file:
```bash
nano config/config.yaml
```
Paste the following contents:
```yaml
# EnviroPulse Configuration

database_path: "/mnt/weather_db/weather_station.db"

sample_interval_sec: 300

daily_summary_time: "00:00"

gps:
  port: "/dev/serial0"
  baud_rate: 9600

wind:
  anem_pin: 17
  cups_to_mph_factor: 2.4
  adc_channel: 0
  adc_vref: 3.3

sea_level_pressure_hpa: 1013.25

flask:
  host: "0.0.0.0"
  port: 8090
```
Save and exit (Ctrl+O, Enter, Ctrl+X).

---

### Step 3: Populate `scripts/setup.sh`
Create the setup script:
```bash
nano scripts/setup.sh
```
Paste the following contents:
```bash
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
