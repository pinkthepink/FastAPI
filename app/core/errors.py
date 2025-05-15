from typing import Any, Dict, List, Optional, Union

class AppError(Exception):
    """Base exception class for application errors."""
    
    def __init__(
        self, 
        message: str = "An unexpected error occurred", 
        status_code: int = 500,
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppError):
    """Exception raised when a resource is not found."""
    
    def __init__(
        self, 
        message: str = "Resource not found", 
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        super().__init__(message=message, status_code=404, details=details)


class ValidationError(AppError):
    """Exception raised when input validation fails."""
    
    def __init__(
        self, 
        message: str = "Validation error", 
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        super().__init__(message=message, status_code=400, details=details)


class DatabaseError(AppError):
    """Exception raised when a database operation fails."""
    
    def __init__(
        self, 
        message: str = "Database operation failed", 
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        super().__init__(message=message, status_code=500, details=details)


class DuplicateError(AppError):
    """Exception raised when trying to create a duplicate resource."""
    
    def __init__(
        self, 
        message: str = "Resource already exists", 
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        super().__init__(message=message, status_code=409, details=details)


class UnauthorizedError(AppError):
    """Exception raised when authentication fails."""
    
    def __init__(
        self, 
        message: str = "Authentication required", 
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        super().__init__(message=message, status_code=401, details=details)


class ForbiddenError(AppError):
    """Exception raised when a user doesn't have permission for an action."""
    
    def __init__(
        self, 
        message: str = "Access forbidden", 
        details: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None
    ):
        super().__init__(message=message, status_code=403, details=details)