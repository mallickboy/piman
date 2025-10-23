from typing import Union
import psutil
import logging
import time
from config import (
    LOGGING_ENABLED,
    LOG_FILE_OS_INFO,
    FETCH_INTERVAL
)

# Configure logging
if LOGGING_ENABLED:
    logging.basicConfig(
        filename=LOG_FILE_OS_INFO,
        level=logging.INFO,  # Enable logging
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        filename=LOG_FILE_OS_INFO,
        level=logging.NOTSET,  # Disable logging
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

GB_TO_BYTES = 1024 ** 3  # 1 GB = 1024^3 bytes
MB_TO_BYTES = 1024 ** 2  # 1 MB = 1024^2 bytes

def get_cpu_usage() -> float:
    """Returns the current CPU usage in percentage."""
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        logging.error(f"Error getting CPU usage: {e}")
        return None

def get_ram_info(decimal: int = 2) -> dict[str, float]:
    """Returns RAM usage details including used, active, and total memory in GB."""
    try:
        memory = psutil.virtual_memory()
        memory_info = {
            "used": round(memory.used / GB_TO_BYTES, decimal),
            "active": round(memory.active / GB_TO_BYTES, decimal),
            "total": round(memory.total / GB_TO_BYTES, decimal)
        }
        return memory_info
    except Exception as e:
        logging.error(f"Error getting RAM info: {e}")
        return {"used": None, "active": None, "total": None}

def get_active_threads() -> int:
    """Returns the total number of active threads across all processes."""
    try:
        return sum(p.num_threads() for p in psutil.process_iter())
    except Exception as e:
        logging.error(f"Error getting active threads: {e}")
        return None

def get_total_process() -> int:
    """Returns the total number of processes running on the system."""
    try:
        return len(psutil.pids())
    except Exception as e:
        logging.error(f"Error getting total processes: {e}")
        return None

def get_network_info(decimal: int = 2) -> dict[str, Union[int, float]]:
    """Returns network statistics: sent, received data in MB and active connections."""
    try:
        net_io = psutil.net_io_counters()
        network_info = {
            "send": round(net_io.bytes_sent / MB_TO_BYTES, decimal),
            "receive": round(net_io.bytes_recv / MB_TO_BYTES, decimal),
            "connection": len(psutil.net_connections())
        }
        return network_info
    except Exception as e:
        logging.error(f"Error getting network info: {e}")
        return {"send": None, "receive": None, "connection": None}
    
def get_uptime(decimal: int = 2) -> float:
    """Returns the system uptime in hours."""
    try:
        boot_time = psutil.boot_time()  # Get system boot time (seconds since epoch)
        current_time = time.time()  # Current time in seconds since epoch
        uptime_seconds = current_time - boot_time  # Calculate uptime in seconds
        # print(uptime_seconds)
        uptime_hours = uptime_seconds / 3600  # Convert seconds to hours
        return round(uptime_hours, decimal)
    except Exception as e:
        logging.error(f"Error getting uptime: {e}")
        return None

def get_system_info() -> dict[str, any]:
    """Returns a summary of the system's CPU, RAM, processes, threads, and network info."""

    os_info = {
        "uptime": get_uptime(),
        "process": get_total_process(),
        "thread": get_active_threads(),
        "cpu": get_cpu_usage(),
        "ram": get_ram_info(),
        "network": get_network_info()
    }
    return os_info

if __name__ == "__main__":
    from time import sleep
    while True:
        system_info = get_system_info()
        print(system_info)
        logging.info(system_info)
        sleep(FETCH_INTERVAL)