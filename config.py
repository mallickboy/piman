"""Config script to load environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv


if os.path.exists(".env"):
    env_path = Path(".env")
elif os.path.exists(".env.defaults"):
    env_path = Path(".env.defaults")
else:
    env_path = None

if env_path:
    load_dotenv(dotenv_path=env_path)
else:
    print("[info] No .env or .env.defaults found.... \nUsing internal defaults.")

# General config
IS_RUNNING = bool(os.getenv("IS_RUNNING") or False)
START_DELAY = int(os.getenv("START_DELAY") or 300)
SNOOZE_TIME = int(os.getenv("SNOOZE_TIME") or 300)
AC_SIGNAL_PIN = int(os.getenv("AC_SIGNAL_PIN") or 27)
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL") or 5)
PUBLISH_INFO = bool(os.getenv("IS_RUNNING") or False)
PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL") or 60)
RPI_FAN_SPEED_FILE = Path(os.getenv("RPI_FAN_SPEED_FILE", "/sys/devices/platform/cooling_fan/hwmon/hwmon2/fan1_input"))
RPI_FAN_PWM_FILE = Path(os.getenv("RPI_FAN_PWM_FILE", "/sys/devices/platform/cooling_fan/hwmon/hwmon2/pwm1"))

# Log Config
LOGGING_ENABLED = bool(os.getenv("LOGGING_ENABLED") or True)

LOG_FILE_AC_INFO = os.getenv("LOG_FILE_AC_INFO") or "piman/ac_info.log"
LOG_FILE_OS_INFO = os.getenv("LOG_FILE_OS_INFO") or "piman/os_info.log"
LOG_FILE_HW_INFO = os.getenv("LOG_FILE_HW_INFO") or "piman/hw_info.log"

# Create log files if not already exists
for log_file in [LOG_FILE_AC_INFO, LOG_FILE_OS_INFO, LOG_FILE_HW_INFO]:
    log_path = Path(log_file)

    try:
        if not log_path.parent.exists():
            print(f"Creating directory: {log_path.parent}")
            log_path.parent.mkdir(parents=True, exist_ok=True)

        if not log_path.exists():
            print(f"Creating log file: {log_path}")
            log_path.touch()
            
    except Exception as e:
        print(f"Error while creating log file {log_path}: {e}")