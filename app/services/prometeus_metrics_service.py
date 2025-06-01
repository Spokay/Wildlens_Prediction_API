import psutil
from prometheus_client import Gauge

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import Info
from pynvml import nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, \
    nvmlDeviceGetMemoryInfo, nvmlInit, nvmlSystemGetDriverVersion, nvmlShutdown

from app.config import logger

CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
GPU_USAGE = Gauge('process_gpu_usage', 'Current GPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')
MEMORY_USAGE_PERCENT = Gauge('process_memory_usage_percent', 'Current memory usage in percent')

def init_nvml():
    try:
        nvmlInit()
        driver_version = nvmlSystemGetDriverVersion()

        logger.info(f"NVML Driver Version: {driver_version}")
    except Exception as e:
        logger.error(f"Failed to initialize NVML: {e}")
        raise RuntimeError("NVML initialization failed") from e

def shutdown_nvml():
    try:
        nvmlShutdown()
        logger.info("NVML shutdown successfully.")
    except Exception as e:
        logger.error(f"Failed to shutdown NVML: {e}")
        raise RuntimeError("NVML shutdown failed") from e


def update_system_metrics(info: Info):

    devices = nvmlDeviceGetCount()

    for i in range(devices):
        handle = nvmlDeviceGetHandleByIndex(i)
        utilization = nvmlDeviceGetUtilizationRates(handle)
        memory_info = nvmlDeviceGetMemoryInfo(handle)
        memory_usage_percent = (memory_info.used / memory_info.total) * 100

        GPU_USAGE.set(utilization.gpu)
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(memory_info.used)
        MEMORY_USAGE_PERCENT.set(memory_usage_percent)

def create_instrumentator() -> Instrumentator:
    instrumentator = Instrumentator()
    instrumentator.add(update_system_metrics)
    return instrumentator



