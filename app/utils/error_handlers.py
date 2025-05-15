from typing import Any, Dict, List, Optional, Tuple, Union
from fastapi import status
from pymongo.errors import DuplicateKeyError, PyMongoError
from pydantic import ValidationError as PydanticValidationError

from app.core.errors import (
    PetshopException,
    ValidationError,
    NotFoundError,
    DuplicateError,
    DatabaseError
)

def handle_api_error(
    error: Exception, 
    message: str = "Erro na operação"
) -> Tuple[Dict[str, Any], int]:
    """
    Centralized error handler for API operations.
    Returns a tuple of (error_response, status_code)
    """
    # Already handled PetshopException - just return it
    if isinstance(error, PetshopException):
        return {"error": error.message, "details": error.details}, error.status_code
        
    # ValidationError from Pydantic
    if isinstance(error, PydanticValidationError):
        validation_error = ValidationError(
            message="Dados inválidos",
            details=[{"loc": err["loc"], "msg": err["msg"]} for err in error.errors()]
        )
        return {"error": validation_error.message, "details": validation_error.details}, validation_error.status_code
        
    # MongoDB Duplicate Key Error
    if isinstance(error, DuplicateKeyError):
        duplicate_error = DuplicateError("Registro duplicado")
        return {"error": duplicate_error.message}, duplicate_error.status_code
        
    # MongoDB Error
    if isinstance(error, PyMongoError):
        db_error = DatabaseError(f"{message}: {str(error)}")
        return {"error": db_error.message}, db_error.status_code
        
    # Default - 500 error
    return {"error": f"{message}: {str(error)}"}, status.HTTP_500_INTERNAL_SERVER_ERROR