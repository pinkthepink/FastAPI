import logging
import time
from typing import Callable, Optional
from uuid import uuid4

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

logger = logging.getLogger(__name__)

# OAuth2 token URL for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/auth/login")


async def get_request_id(
    x_request_id: Optional[str] = Header(None)
) -> str:
    """
    Get or generate a request ID for tracking.
    
    Args:
        x_request_id: Optional request ID from header
        
    Returns:
        str: The request ID
    """
    if x_request_id:
        return x_request_id
    return str(uuid4())


def log_request_time() -> Callable:
    """
    Create a dependency for logging request processing time.
    
    Returns:
        Callable: A dependency function for timing requests
    """
    
    async def _log_request_time(request: Request) -> None:
        """
        Measure and log the request processing time.
        
        Args:
            request: The FastAPI request object
        """
        request.state.start_time = time.time()
        
        # This will be called after the request is processed
        yield
        
        process_time = time.time() - request.state.start_time
        logger.info(
            f"Request processed in {process_time:.4f} seconds",
            extra={
                "path": request.url.path,
                "method": request.method,
                "processing_time": process_time,
                "request_id": request.headers.get("X-Request-ID"),
            },
        )
    
    return _log_request_time