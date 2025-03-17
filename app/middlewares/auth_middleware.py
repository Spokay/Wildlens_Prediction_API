from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import IGNORED_API_KEY_MIDDLEWARE_PATHS, WILDLENS_PREDICTION_API_KEY
from app.services.auth_service import extract_api_key


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if  request.url.path.startswith(tuple(IGNORED_API_KEY_MIDDLEWARE_PATHS)):
            return await call_next(request)
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