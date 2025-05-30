import psutil
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator
from pynvml import nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, \
    nvmlDeviceGetMemoryInfo

CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
GPU_USAGE = Gauge('process_gpu_usage', 'Current GPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')


def update_system_metrics():
    devices = nvmlDeviceGetCount()

    for i in range(devices):
        handle = nvmlDeviceGetHandleByIndex(i)
        utilization = nvmlDeviceGetUtilizationRates(handle)
        memory_info = nvmlDeviceGetMemoryInfo(handle)

        GPU_USAGE.set(utilization.gpu)
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(memory_info.used)

def create_instrumentator() -> Instrumentator:
    instrumentator = Instrumentator()
    instrumentator.add(update_system_metrics())
    return instrumentator



