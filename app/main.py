from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from pynvml import nvmlInit, nvmlSystemGetDriverVersion, nvmlShutdown

from app.config import logger
from app.middlewares.auth_middleware import AuthMiddleware
from app.middlewares.exception_logging_middleware import ExceptionLoggingMiddleware



import os

from app.routes.prediction_routes import router as prediction_router
from app.routes.metrics_routes import router as metrics_router

import uvicorn
from fastapi import FastAPI, WebSocket

@asynccontextmanager
async def lifespan(app_object: FastAPI):
    # Executed before startup (setup):
    nvmlInit()
    logger.info('Initialized Nvml with Nvidia driver version = %s', nvmlSystemGetDriverVersion())
    # ------------------------------
    yield  # <--- This is where the context manager pauses and the application starts
    # ------------------------------
    # Executed after shutdown (cleanup):
    nvmlShutdown()
    #

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(prediction_router)
app.include_router(metrics_router)

# setting up logging middleware

app.add_middleware(AuthMiddleware)
app.add_middleware(ExceptionLoggingMiddleware)


if __name__ == "__main__":
    port = int(os.getenv("WILDLENS_PREDICTION_API_PORT", 5001))
    assert os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH") is not None
    assert os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH") is not None
    uvicorn.run(app, host="127.0.0.1", port=int(port))
