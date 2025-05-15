import logging
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from pymongo.errors import DuplicateKeyError

from app.core.errors import (
    AppError,
    DatabaseError,
    DuplicateError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

logger = logging.getLogger(__name__)

def format_error_response(
    status_code: int,
    message: str,
    details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Format standardized error response."""
    error_response = {
        "status_code": status_code,
        "message": message,
    }
    
    if details:
        error_response["details"] = details
    
    if request_id:
        error_response["request_id"] = request_id
    
    return error_response


def setup_error_handlers(app: FastAPI) -> None:
    """Set up global exception handlers for the application."""
    
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        """Handle application-specific exceptions."""
        logger.error(
            f"Application error: {exc.message}",
            extra={
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path,
            },
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(
                status_code=exc.status_code,
                message=exc.message,
                details=exc.details,
                request_id=request.headers.get("X-Request-ID"),
            ),
        )
    
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle FastAPI request validation errors."""
        logger.warning(
            "Request validation error",
            extra={
                "path": request.url.path,
                "details": exc.errors(),
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=format_error_response(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Validation error",
                details=exc.errors(),
                request_id=request.headers.get("X-Request-ID"),
            ),
        )
    
    @app.exception_handler(PydanticValidationError)
    async def handle_pydantic_validation_error(
        request: Request, exc: PydanticValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        logger.warning(
            "Pydantic validation error",
            extra={
                "path": request.url.path,
                "details": exc.errors(),
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=format_error_response(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Validation error",
                details=exc.errors(),
                request_id=request.headers.get("X-Request-ID"),
            ),
        )
    
    @app.exception_handler(DuplicateKeyError)
    async def handle_duplicate_key_error(
        request: Request, exc: DuplicateKeyError
    ) -> JSONResponse:
        """Handle MongoDB duplicate key errors."""
        logger.warning(
            "Duplicate key error",
            extra={
                "path": request.url.path,
                "details": str(exc),
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=format_error_response(
                status_code=status.HTTP_409_CONFLICT,
                message="Resource already exists",
                details=str(exc),
                request_id=request.headers.get("X-Request-ID"),
            ),
        )
    
    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle any unhandled exceptions."""
        logger.exception(
            f"Unhandled exception: {str(exc)}",
            extra={
                "path": request.url.path,
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=format_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
                request_id=request.headers.get("X-Request-ID"),
            ),
        )