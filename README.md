# Raspberry Pi Environmental Monitor

A live environmental monitoring system built on a Raspberry Pi 4 with a Pimoroni Enviro+ board and PMS5003 particulate sensor. Sensor data is collected, stored in PostgreSQL, and served through a public dashboard at [alecvolkertenvironment.com](https://alecvolkertenvironment.com).

## Hardware

- Raspberry Pi 4
- Pimoroni Enviro+ (BME280, MICS6814, LTR559)
- PMS5003 particulate matter sensor

## What it measures

| Sensor | Measurements |
|--------|-------------|
| BME280 | Temperature, humidity, pressure |
| MICS6814 | Oxidising (NO2), reducing (CO), NH3 |
| PMS5003 | PM1.0, PM2.5, PM10 |
| LTR559 | Light level |


## Sensor drivers

All sensor drivers were implemented from scratch using datasheets — no third party sensor libraries. This includes:

- BME280 I2C calibration register parsing, two's complement signed conversion, and Bosch compensation formulas
- MICS6814 gas sensor via ADS1015 ADC — config register bit manipulation, voltage divider math, resistance calculation
- PMS5003 UART binary protocol — start byte synchronization, big-endian packet parsing, checksum verification

## Running
```bash
pip install -r requirements.txt
python3 main.py
```

Requires a `.env` file with database credentials and API key — see `.env.example`.

## Motivation

Built as a personal project at the intersection of climate tech and systems programming. Air quality monitoring at the neighborhood level is an underserved problem — this project is a small contribution toward making that data more accessible.
