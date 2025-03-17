import traceback

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import logger


class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
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
