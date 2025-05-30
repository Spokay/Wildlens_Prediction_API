from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings
from app.services.auth_service import extract_api_key

settings = get_settings()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if  request.url.path.startswith(tuple(settings.excluded_paths)):
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key is required"
            )

        api_key = extract_api_key(auth_header)

        if api_key != settings.wildlens_prediction_api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key"
            )

        response = await call_next(request)
        return response