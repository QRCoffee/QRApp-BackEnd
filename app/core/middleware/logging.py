from loguru import logger
import time
from app.core.config import settings
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        # ---- Extract information of request
        method = request.method
        path = request.url.path
        host = request.client.host
        status_code = response.status_code
        # --- Log
        logger.info({
            "host": host,
            "method": method,
            "path": path,
            "duration": duration,
            "status_code": status_code,
        })
        return response