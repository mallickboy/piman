import RPi.GPIO as GPIO
import time
import logging
from config import (
    AC_SIGNAL_PIN,
    LOGS_ACTIVE,
    LOGGING_ENABLED,
    LOG_FILE_AC_INFO
)

# Configure logging
if LOGGING_ENABLED:
    logging.basicConfig(
        filename=LOG_FILE_AC_INFO,
        level=logging.INFO,  # Enable logging
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        filename=LOG_FILE_AC_INFO,
        level=logging.NOTSET,  # Disable logging
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

ac_is_available = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(AC_SIGNAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def get_ac_info():
    "Returns Ture if AC_SIGNAL_PIN is HIGH"
    try:
        return {"electricity" : bool(GPIO.input(AC_SIGNAL_PIN))}
    except Exception as e:
        logging.error(f"Error getting CPU temperature: {e}")
        return {"electricity" : False}

if __name__=="__main__":
    from time import sleep
    try:
        while True:
            ac_info = get_ac_info()
            print(ac_info)
            logging.info(ac_info)
            time.sleep(60)
    finally:
        GPIO.cleanup()
