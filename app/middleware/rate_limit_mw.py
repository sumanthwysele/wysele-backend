import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# { ip: [timestamp, timestamp, ...] }
request_counts: dict = defaultdict(list)

# General API: 100 requests per minute
GENERAL_LIMIT = 100
GENERAL_WINDOW = 60

# Login endpoint: 5 attempts per minute (brute-force protection)
LOGIN_LIMIT = 5
LOGIN_WINDOW = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()
        path = request.url.path

        is_login = path.endswith("/auth/login")
        limit = LOGIN_LIMIT if is_login else GENERAL_LIMIT
        window = LOGIN_WINDOW if is_login else GENERAL_WINDOW

        key = f"{ip}:{path}" if is_login else ip

        # Remove timestamps outside the current window
        request_counts[key] = [t for t in request_counts[key] if now - t < window]

        if len(request_counts[key]) >= limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."}
            )

        request_counts[key].append(now)
        return await call_next(request)
