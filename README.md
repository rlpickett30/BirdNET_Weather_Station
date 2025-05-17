# Weather_Station
A compact weather station for Raspberry Pi, integrating BirdNET for bird call identification alongside precise environmental monitoring, including temperature, humidity, barometric pressure, dew point, and storm alerts. Ideal for nature enthusiasts and researchers.
# BirdNET Weather Station

## Features

* **Temperature Monitoring:** Real-time ambient temperature readings.
* **Humidity Measurement:** Accurate humidity data for climate tracking.
* **Barometric Pressure:** Atmospheric pressure monitoring with storm alert capabilities.
* **Dew Point Calculation:** Automatic dew point estimation.
* **Altitude Estimation:** Altitude based on pressure for enhanced data analysis.
* **Seamless Daily Brief Integration:** Syncs with the Daily Brief script for automated weather updates.
* **Local Network Access:** View real-time data through a web interface via `birdpi.local`.

## Hardware Requirements

* Raspberry Pi (Model 4 recommended)
* MicroSD Card (Max Endurance recommended)
* Adafruit BMP390 sensor (barometric pressure and temperature)
* Adafruit SHT31 sensor (temperature and humidity)
* Heatsink (recommended for temperature stability)
* Power Supply (minimum 3A)
* Internet Connection (WiFi or Ethernet)

## Software Requirements

* Raspberry Pi OS (64-bit recommended)
* Python 3.11+
* Git (for version control)
* BirdNET-Pi Installation

## Setup Steps

### 1. Prepare the Raspberry Pi

* Flash Raspberry Pi OS to the microSD card.
* Boot the Raspberry Pi and connect to WiFi.
* Run initial system updates:

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Git and Clone Repository

* Install Git if not already installed:

```bash
sudo apt install git -y
```

* Clone this repository:

```bash
git clone https://github.com/<your-username>/birdnet-weather-station.git
cd birdnet-weather-station
```

### 3. Install Required Python Libraries

Install the required Python libraries for sensor data collection and processing:

```bash
pip install adafruit-circuitpython-bmp3xx adafruit-circuitpython-sht31d requests
```

### 4. Connect the Sensors

* **BMP390:** Connect the BMP390 to the I2C pins on the Raspberry Pi.
* **SHT31:** Connect the SHT31 to the I2C pins as well.
* Enable the I2C interface:

```bash
sudo raspi-config
```

* Select **Interface Options** → **I2C** → **Enable**.

### 5. Test the Sensors

Run a simple script to verify the sensors are detected:

```bash
i2cdetect -y 1
```

You should see the sensor addresses (typically 0x77 for BMP390 and 0x44 for SHT31) in the output.

### 6. Run the Weather Station Script

Run the main weather station script:

```bash
python3 weather_station.py
```

### 7. Integrate with BirdNET

* Follow the BirdNET setup guide to ensure the BirdNET server is running on the same Raspberry Pi.

### 8. Set Up Daily Brief Integration

* Ensure the weather station data can be accessed by your existing Daily Brief script.

### 9. (Optional) Set Up Local Network Access

* Configure your Pi to be accessible via `birdpi.local`.

### 10. Finalize and Test

* Reboot the Pi and verify the weather station runs on startup.
* Test data logging and real-time access through your browser.

## Future Improvements

* Solar Power Integration
* Long-term Data Storage
* Enhanced Data Visualizations

## License

MIT License

---

Feel free to reach out for support or contribute to this project!
