from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Force HTTPS on all future requests for 1 year
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # Prevent browsers from sniffing content type
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Block clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"
        # Disable browser XSS filter (modern CSP replaces this)
        response.headers["X-XSS-Protection"] = "0"
        # Restrict what resources the browser can load
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "img-src 'self' data: fastapi.tiangolo.com"
        )
        # Don't send referrer info to other domains
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Restrict browser features
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response
