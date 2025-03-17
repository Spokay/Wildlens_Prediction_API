from prometheus_client import Gauge
from pynvml import *

from app.config import logger

CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
GPU_USAGE = Gauge('process_gpu_usage', 'Current GPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')


async def start_nvml():
    device = nvmlDeviceGetHandleByIndex(0)
    try:
        logger.info("Initializing nvml")
        nvmlInit()

        logger.info('Started with Nvidia driver version = %s', nvmlSystemGetDriverVersion())

    except Exception as e:
        logger.info('Exception thrown - %s', e, exc_info=True)

    finally:
        nvmlShutdown()

def update_system_metrics():
    pass