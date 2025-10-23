# 🖥️ PiMan — Raspberry Pi System Monitor

A lightweight Python-based utility to monitor **hardware** and **system performance** metrics on a Raspberry Pi or Linux system.  
It logs temperature, voltage, clock speed, fan stats, CPU usage, RAM utilization, network traffic, and uptime — all configurable via environment variables.

---

## 🚀 Features

- 🧠 CPU monitoring — usage %, clock speed (GHz), voltage  
- 🌡️ Temperature tracking — live CPU temp (via `vcgencmd`)  
- 🌬️ Fan monitoring — PWM and RPM readings  
- 💾 System stats — RAM, uptime, threads, and process count  
- 🌐 Network metrics — sent/received MB and active connections  
- 🪵 Structured logging to file  
- ⚙️ Configurable via `.env` or fallback defaults  
- 🔄 Runs continuously at a defined fetch interval  

---

## 🧩 Project Structure

```bash
├── config.py
├── hardware_info.py # Hardware metrics (temp, voltage, fan)
├── system_info.py # System metrics (CPU, RAM, network)
├── .env.defaults # Non-secret environment defaults
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Configuration

This project uses `.env` (or `.env.defaults`) for configuration.  
All values are **non-secret** and safe to version-control.

### Example `.env.defaults`

```bash
# Logging
LOGGING_ENABLED=True
LOG_FILE_HW_INFO=logs/hw_info.log
LOG_FILE_OS_INFO=logs/os_info.log

# Fetch interval (in seconds)
FETCH_INTERVAL=5

# Fan sensor paths
RPI_FAN_SPEED_FILE=/sys/devices/platform/rpi_fan/hwmon/hwmon0/fan1_input
RPI_FAN_PWM_FILE=/sys/devices/platform/rpi_fan/hwmon/hwmon0/pwm1
```

You can copy .env.defaults to .env if you wish to customize values locally.

The application will:

- Load .env if it exists

- Fall back to .env.defaults

- Use internal defaults if neither file is found

## 📜 License
This project is licensed under the Apache License 2.0.

## ⚙️ Version
Version 0: Currently under active development 🚧