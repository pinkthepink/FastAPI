import logging
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.api_router import api_router
from app.core.config import settings
from app.database.mongodb import create_indexes, lifespan
from app.utils.error_handlers import setup_error_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create FastAPI app
app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    lifespan=lifespan,
)

# Setup error handlers
setup_error_handlers(app)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next: Callable) -> Response:
    """Add a unique request ID to each request if not present."""
    if not request.headers.get("X-Request-ID"):
        request.headers.__dict__["_list"].append(
            (b"x-request-id", f"{time.time():.9f}".encode())
        )
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.headers.get("X-Request-ID")
    return response


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    """Add processing time header to response."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    """Log all requests with path and method."""
    logger = logging.getLogger("app.request")
    
    logger.info(
        f"Request: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client": request.client.host if request.client else None,
            "request_id": request.headers.get("X-Request-ID"),
        },
    )
    
    response = await call_next(request)
    
    logger.info(
        f"Response: {response.status_code} for {request.method} {request.url.path}",
        extra={
            "status_code": response.status_code,
            "method": request.method,
            "path": request.url.path,
            "request_id": request.headers.get("X-Request-ID"),
        },
    )
    
    return response


# Include API router
app.include_router(api_router, prefix=settings.api_v1_str)


@app.on_event("startup")
async def startup_event():
    """Execute startup actions like creating indexes."""
    await create_indexes()


@app.get("/")
def root():
    """Root endpoint that redirects to docs."""
    return JSONResponse(
        content={
            "message": "Client Management API",
            "docs_url": "/docs",
            "openapi_url": "/openapi.json",
        }
    )