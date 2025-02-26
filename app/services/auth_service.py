import traceback

from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import WILDLENS_PREDICTION_API_KEY, logger


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


class ExceptionHandlerLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            logger.info(f"HTTP error: {http_exc.detail} (status: {http_exc.status_code})")
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail}
            )
        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            logger.debug(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred."}
            )
