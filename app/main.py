from dotenv import load_dotenv

load_dotenv()

import os
from app.services.auth_service import AuthMiddleware

from app.routes.prediction_routes import router

import uvicorn
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)

app.add_middleware(AuthMiddleware)


if __name__ == "__main__":
    port = int(os.getenv("WILDLENS_PREDICTION_API_PORT", 5001))
    assert os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH") is not None
    assert os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH") is not None
    uvicorn.run(app, host="127.0.0.1", port=int(port))
