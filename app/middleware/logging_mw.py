import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api_logger")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 1. Capture request details
        method = request.method
        url = request.url.path
        client_host = request.client.host
        
        # 2. Process the request
        response = await call_next(request)
        
        # 3. Calculate processing time
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}ms".format(process_time)
        
        # 4. Log the audit data
        # Example: INFO: 127.0.0.1 - POST /api/v1/blogs/ - 201 Created (14.5ms)
        logger.info(
            f"{client_host} - {method} {url} - "
            f"{response.status_code} - {formatted_process_time}"
        )
        
        # Add the timing to the response header (useful for debugging)
        response.headers["X-Process-Time"] = formatted_process_time
        
        return response