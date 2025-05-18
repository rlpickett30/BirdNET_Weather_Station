# EnviroPulse

**A minimalist Raspberry Pi weather station**  
Records environmental data every five minutes and serves a simple web GUI.

## Features
- Timestamped readings of:
  - GPS (latitude, longitude)
  - Temperature (°C)
  - Humidity (%)
  - Dew point (°C)
  - Barometric pressure (hPa)
  - Altitude (m)
  - Wind speed (m/s)
  - Wind direction (° clockwise from true north)
- Daily summary at midnight:
  - Plots for temperature, humidity, and wind speed
  - Polar plot of wind direction
  - High/low stats for temperature and humidity
- Data stored in SQLite and visible via a minimalist Flask GUI

## Repository Structure

