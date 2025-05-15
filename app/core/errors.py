from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, status

class PetshopException(Exception):
    """Base exception for Petshop application errors"""
    
    def __init__(
        self, 
        message: str = "An error occurred", 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Union[List[Any], Dict[str, Any]]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


# Validation error
class ValidationError(PetshopException):
    def __init__(self, message: str = "Dados inválidos", details: Optional[List[Dict[str, Any]]] = None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, details=details)


# Not found error
class NotFoundError(PetshopException):
    def __init__(self, entity: str):
        super().__init__(
            message=f"{entity} não encontrado",
            status_code=status.HTTP_404_NOT_FOUND
        )


# Duplicate record error
class DuplicateError(PetshopException):
    def __init__(self, message: str = "Registro duplicado"):
        super().__init__(
            message=message, 
            status_code=status.HTTP_409_CONFLICT
        )


# Database error
class DatabaseError(PetshopException):
    def __init__(self, message: str = "Erro na operação de banco de dados"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Authentication error
class AuthenticationError(PetshopException):
    def __init__(self, message: str = "Falha na autenticação"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


# Authorization error
class AuthorizationError(PetshopException):
    def __init__(self, message: str = "Não autorizado"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )