from time import sleep
from watchdogs.os_info import get_system_info
from watchdogs.hw_info import get_hardware_info

while True:
    try:
        hw = get_hardware_info()
        os = get_system_info()
        print(hw, os)
        sleep(1)
    except KeyboardInterrupt:
        print("\tProgramme Ended Successfully")
        break
