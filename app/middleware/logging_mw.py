import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api_logger")
security_logger = logging.getLogger("security_logger")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        path = request.url.path
        ip = request.client.host

        response = await call_next(request)

        process_time = "{0:.2f}ms".format((time.time() - start_time) * 1000)
        status = response.status_code

        # General request log
        logger.info(f"{ip} - {method} {path} - {status} - {process_time}")

        # Security event logging
        if status == 401:
            security_logger.warning(f"[UNAUTHORIZED] {ip} - {method} {path}")
        elif status == 403:
            security_logger.warning(f"[FORBIDDEN] {ip} - {method} {path}")
        elif status == 429:
            security_logger.warning(f"[RATE LIMITED] {ip} - {method} {path}")
        elif path.endswith("/auth/login") and method == "POST":
            if status == 200:
                security_logger.info(f"[LOGIN SUCCESS] {ip} - {path}")
            else:
                security_logger.warning(f"[LOGIN FAILED] {ip} - {path} - status {status}")

        response.headers["X-Process-Time"] = process_time
        return response
