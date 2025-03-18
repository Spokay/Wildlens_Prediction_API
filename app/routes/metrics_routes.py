import psutil
from fastapi import APIRouter
from prometheus_client import Gauge, generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from pynvml import *
from starlette.responses import Response

CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
GPU_USAGE = Gauge('process_gpu_usage', 'Current GPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')


router = APIRouter()

def update_system_metrics():
    devices = nvmlDeviceGetCount()

    for i in range(devices):
        handle = nvmlDeviceGetHandleByIndex(i)
        utilization = nvmlDeviceGetUtilizationRates(handle)
        memory_info = nvmlDeviceGetMemoryInfo(handle)

        GPU_USAGE.set(utilization.gpu)
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(memory_info.used)


@router.get(
    "/metrics",
    description="Endpoint to retrieve prometeus metrics",
)
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
