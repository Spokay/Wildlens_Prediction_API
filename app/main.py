from dotenv import load_dotenv

from app.middlewares.auth_middleware import AuthMiddleware
from app.middlewares.exception_logging_middleware import ExceptionLoggingMiddleware

load_dotenv()

import os

from app.routes.prediction_routes import router

import uvicorn
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)

# setting up logging middleware

app.add_middleware(AuthMiddleware)
app.add_middleware(ExceptionLoggingMiddleware)

if __name__ == "__main__":
    port = int(os.getenv("WILDLENS_PREDICTION_API_PORT", 5001))
    assert os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH") is not None
    assert os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH") is not None
    uvicorn.run(app, host="127.0.0.1", port=int(port))
