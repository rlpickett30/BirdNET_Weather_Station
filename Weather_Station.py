import time
import board
import adafruit_bmp3xx
import adafruit_sht31d
import json
import os
from datetime import datetime

# Initialize I2C bus
i2c = board.I2C()

# Initialize sensors
bmp390 = adafruit_bmp3xx.BMP3XX_I2C(i2c)
sht31 = adafruit_sht31d.SHT31D(i2c)

# Set BMP390 parameters
bmp390.pressure_oversampling = 8
bmp390.temperature_oversampling = 2

# Track daily high and low temperatures
daily_high = float('-inf')
daily_low = float('inf')
daily_humidity_high = float('-inf')
daily_humidity_low = float('inf')
last_reset_date = datetime.now().date()

# Pressure tracking for storm detection
last_pressure = None
pressure_trend = []
TREND_WINDOW = 12  # 1 hour (5 min * 12)
PRESSURE_DROP_THRESHOLD = 3.0  # hPa

# Storage paths
DATA_DIR = "/home/pi/weather_data"
DAILY_LOG_DIR = os.path.join(DATA_DIR, "daily_logs")
HOURLY_LOG_FILE = os.path.join(DATA_DIR, "hourly_log.json")

# Create directories if they don't exist
os.makedirs(DAILY_LOG_DIR, exist_ok=True)

# Define constants for altitude calculation
SEA_LEVEL_PRESSURE = 1013.25  # hPa

# Read and average data
def get_weather_data():
    global daily_high, daily_low, daily_humidity_high, daily_humidity_low, last_reset_date, last_pressure, pressure_trend
    temp_bmp = bmp390.temperature  # Temperature from BMP390 (C)
    temp_sht = sht31.temperature  # Temperature from SHT31 (C)
    humidity = sht31.relative_humidity  # Humidity (%)
    pressure = bmp390.pressure  # Barometric pressure (hPa)

    # Calculate average temperature
    avg_temp = (temp_bmp + temp_sht) / 2

    # Calculate altitude using the barometric formula
    altitude = 44330 * (1.0 - (pressure / SEA_LEVEL_PRESSURE) ** (1/5.255))

    # Calculate dew point
    a = 17.27
    b = 237.7
    alpha = ((a * avg_temp) / (b + avg_temp)) + (humidity / 100.0)
    dew_point = (b * alpha) / (a - alpha)

    # Update daily high and low for temperature and humidity
    if avg_temp > daily_high:
        daily_high = avg_temp
    if avg_temp < daily_low:
        daily_low = avg_temp
    if humidity > daily_humidity_high:
        daily_humidity_high = humidity
    if humidity < daily_humidity_low:
        daily_humidity_low = humidity

    # Pressure trend detection
    if last_pressure is not None:
        pressure_change = pressure - last_pressure
        pressure_trend.append(pressure_change)
        if len(pressure_trend) > TREND_WINDOW:
            pressure_trend.pop(0)
        # Check for significant pressure drop indicating possible storm
        if sum(pressure_trend) <= -PRESSURE_DROP_THRESHOLD:
            print("⚠️ Possible storm detected: Significant pressure drop in the last hour.")
    last_pressure = pressure

    # Check for date rollover to reset high/low and log daily summary
    current_date = datetime.now().date()
    if current_date != last_reset_date:
        # Log daily data
        daily_filename = os.path.join(DAILY_LOG_DIR, f"{last_reset_date}.json")
        daily_data = {
            "date": last_reset_date.strftime("%Y-%m-%d"),
            "high_temp": round(daily_high, 2),
            "low_temp": round(daily_low, 2),
            "high_humidity": round(daily_humidity_high, 2),
            "low_humidity": round(daily_humidity_low, 2)
        }
        with open(daily_filename, "w") as f:
            json.dump(daily_data, f)
        print(f"Daily summary logged: {daily_data}")

        # Reset for new day
        daily_high = float('-inf')
        daily_low = float('-inf')
        daily_humidity_high = float('-inf')
        daily_humidity_low = float('-inf')
        last_reset_date = current_date

    # Format the hourly data
    hourly_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(avg_temp, 2),
        "humidity": round(humidity, 2),
        "pressure": round(pressure, 2),
        "altitude": round(altitude, 2),
        "dew_point": round(dew_point, 2)
    }

    # Append to the hourly log file
    with open(HOURLY_LOG_FILE, "a") as f:
        json.dump(hourly_data, f)
        f.write("\n")

    return hourly_data

# Write data to a JSON file for the daily brief script to access
def update_weather_file():
    data = get_weather_data()
    with open("/home/pi/weather_data.json", "w") as f:
        json.dump(data, f)
    print(f"Weather data updated: {data}")

if __name__ == "__main__":
    while True:
        update_weather_file()
        time.sleep(300)  # Update every 5 minutes
