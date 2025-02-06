from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import WILDLENS_PREDICTION_API_KEY


def extract_api_key(auth_header):
    try:
        return auth_header.split("Key ")[1]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key is required"
            )

        api_key = extract_api_key(auth_header)

        if api_key != WILDLENS_PREDICTION_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key"
            )

        response = await call_next(request)
        return response