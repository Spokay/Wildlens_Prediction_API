import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WILDLENS_PREDICTION_API_KEY = os.getenv("WILDLENS_PREDICTION_API_KEY")

logger.info(f"Multiclass Classifier model path : {os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH")}")
logger.info(f"Binary classifier model path : {os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH")}")
WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH = os.getenv("WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH")
WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH = os.getenv("WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH")

IGNORED_API_KEY_MIDDLEWARE_PATHS = [
    "/docs",
    "/openapi.json",
    "/metrics"
]