import lgpio
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
GPIO_HANDLE = lgpio.gpioGPIO_HANDLE_open(0)
lgpio.gpio_claim_input(GPIO_HANDLE, AC_SIGNAL_PIN, lgpio.SET_PULL_DOWN)

def get_ac_info():
    "Returns Ture if AC_SIGNAL_PIN is HIGH"
    try:
        return {"electricity" : bool(lgpio.gpio_read(GPIO_HANDLE, AC_SIGNAL_PIN))}
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
            time.sleep(2)
    finally:
        lgpio.gpiochip_close(GPIO_HANDLE)
