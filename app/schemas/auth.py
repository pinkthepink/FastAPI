from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    is_admin: bool = False


class UserBase(BaseModel):
    email: EmailStr
    nome: str
    is_admin: bool = False
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: str = Field(..., alias="_id")
    hashed_password: str


class User(UserBase):
    id: str = Field(..., alias="_id")


class UserLogin(BaseModel):
    email: EmailStr
    password: str