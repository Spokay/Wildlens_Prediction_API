import traceback

from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import WILDLENS_PREDICTION_API_KEY, IGNORED_API_KEY_MIDDLEWARE_PATHS, logger


def extract_api_key(auth_header):
    try:
        return auth_header.split("Key ")[1]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
