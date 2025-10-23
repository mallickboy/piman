import os
import subprocess
import logging
from config import (
    RPI_FAN_SPEED_FILE,
    RPI_FAN_PWM_FILE,
    LOGGING_ENABLED,
    LOG_FILE_HW_INFO,
    FETCH_INTERVAL
    )

# Configure logging
if LOGGING_ENABLED:
    logging.basicConfig(
        filename=LOG_FILE_HW_INFO,
        level=logging.INFO,  # Enable logging
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        filename=LOG_FILE_HW_INFO,
        level=logging.NOTSET,  # Disable logging
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


GHZ_TO_NO = 1_000_000_000

def get_temperature()-> float:
    """Returns the temperature of the Raspberry Pi CPU in Celsius."""
    try:
        temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
        return float(temp.decode().strip().split('=')[1].split("'")[0])
    except Exception as e:
        logging.error(f"Error getting CPU temperature: {e}")
        return None

def get_cpu_voltage(decimal:int = 2) -> float:
    """Returns the CPU voltage in Volts (V)."""
    try:
        voltage = subprocess.check_output("vcgencmd measure_volts", shell=True)
        return round( float(voltage.decode().strip().split('=')[1].split('V')[0]), decimal)
    except Exception as e:
        logging.error(f"Error getting CPU voltage: {e}")
        return None

def get_clock_frequency(decimal: int = 2) -> float:
    """Returns the CPU clock frequency in GHz (rounded to `decimal` decimal places)."""
    try:
        frequency = subprocess.check_output("vcgencmd measure_clock arm", shell=True)
        # print("Clock frequency", frequency)
        frequency_in_hz = int(frequency.decode().strip().split('=')[-1])
        return round(frequency_in_hz / GHZ_TO_NO, decimal)
    except Exception as e:
        logging.error(f"Error getting CPU clock frequency: {e}")
        return None
    
def get_fan_speed() -> int:
    """Returns the fan speed in RPM (revolutions per minute)."""
    try:
        if os.path.exists(RPI_FAN_SPEED_FILE):
            with open(RPI_FAN_SPEED_FILE, "r") as file:
                fan_speed = int(file.read().strip())
            return fan_speed
        else:
            logging.error("Fan speed file not found.")
            return None
    except Exception as e:
        logging.error(f"Error getting fan speed: {e}")
        return None

def get_fan_pwm() -> int:
    """Returns the fan PWM duty cycle (range: 0-255)."""
    try:
        if os.path.exists(RPI_FAN_PWM_FILE):
            with open(RPI_FAN_PWM_FILE, "r") as file:
                fan_speed = int(file.read().strip())
            return fan_speed
        else:
            logging.error("Fan pwm file not found.")
            return None
    except Exception as e:
        logging.error(f"Error getting fan PWM: {e}")
        return None


def get_hardware_info() -> dict[str, any]:
    """Returns a summary of the system's hardware information: CPU temp, voltage, clock, and fan data."""
    hw_info = {
        "temperature": get_temperature(),
        "voltage": get_cpu_voltage(),
        "clock": get_clock_frequency(),
        "fan": {
            "speed": get_fan_speed(),
            "pwm": get_fan_pwm()
        }
    }
    return hw_info

if __name__ == "__main__":
    from time import sleep
    while True:
        hw_info = get_hardware_info()
        print(hw_info)
        logging.info(hw_info)
        sleep(FETCH_INTERVAL)
