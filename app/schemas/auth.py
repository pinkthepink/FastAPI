from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token schema for authentication response."""
    
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""
    
    sub: Optional[str] = None
    exp: Optional[int] = None


class UserLogin(BaseModel):
    """User login schema."""
    
    email: EmailStr
    password: str