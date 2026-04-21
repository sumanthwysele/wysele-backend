from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.v1.api import api_router
from app.db.base import Base  
from app.db.session import engine, SessionLocal
from app.core.config import settings
from app.middleware.logging_mw import LoggingMiddleware
from app.db.init_db import init_db
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

# 1. DATABASE TABLES: Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=settings.PROJECT_NAME, version="1.0.0", routes=app.routes)
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi

# 2. CORS: Securely pull origins from your .env
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 3. LOGGING: Track every request for auditing
app.add_middleware(LoggingMiddleware)

# 4. INITIALIZATION: Run the Root Admin check on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

# 5. ROUTING: Main API endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error on {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please contact support."}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        # Clean up the error message for the frontend
        field = " -> ".join([str(loc) for loc in error["loc"] if loc != "body"])
        message = error["msg"]
        input_type = error.get("type", "unknown")
        
        errors.append({
            "field": field,
            "error_type": input_type,
            "message": f"Invalid input for '{field}': {message}"
        })

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation Failed",
            "missing_or_invalid_fields": errors
        },
    )

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "message": f"{settings.PROJECT_NAME} is running",
        "version": "1.0.0"
    }