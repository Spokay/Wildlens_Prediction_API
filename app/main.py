from dotenv import load_dotenv

from app.middlewares.exception_logging_middleware import ExceptionLoggingMiddleware
from app.services.prometeus_metrics_service import create_instrumentator

load_dotenv()
from contextlib import asynccontextmanager
from pynvml import nvmlInit, nvmlSystemGetDriverVersion, nvmlShutdown

from app.config import logger, get_settings
from app.middlewares.auth_middleware import AuthMiddleware

from app.routes.prediction_routes import router as prediction_router

import uvicorn
from fastapi import FastAPI

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executed before startup (setup):
    try:
        nvmlInit()
        driver_version = nvmlSystemGetDriverVersion()

        logger.info(f"NVML Driver Version: {driver_version}")
    except Exception as e:
        logger.error(f"Failed to initialize NVML: {e}")
        raise RuntimeError("NVML initialization failed") from e
    # ------------------------------
    yield  # <--- This is where the context manager pauses and the application starts
    # ------------------------------
    # Executed after shutdown (cleanup):
    try:
        nvmlShutdown()
        logger.info("NVML shutdown successfully.")
    except Exception as e:
        logger.error(f"Failed to shutdown NVML: {e}")
        raise RuntimeError("NVML shutdown failed") from e



def create_app():
    wildlens_prediction_api_app = FastAPI(root_path=settings.api_prefix, lifespan=lifespan)

    # Exposing Prometheus metrics endpoints
    instrumentator = create_instrumentator()
    instrumentator.instrument(wildlens_prediction_api_app).expose(wildlens_prediction_api_app)

    # Middlewares
    wildlens_prediction_api_app.add_middleware(AuthMiddleware)
    wildlens_prediction_api_app.add_middleware(ExceptionLoggingMiddleware)

    # Routers
    wildlens_prediction_api_app.include_router(prediction_router)

    return wildlens_prediction_api_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=settings.app_port, reload=False)
