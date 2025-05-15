from typing import Optional
from pydantic import BaseModel, Field


class ClienteBase(BaseModel):
    """Base schema for Cliente."""
    nome: str
    telefone: Optional[str] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema for creating a new Cliente."""
    pass


class ClienteUpdate(BaseModel):
    """Schema for updating a Cliente."""
    nome: Optional[str] = None
    telefone: Optional[str] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None


class ClienteInDB(ClienteBase):
    """Schema for Cliente as stored in the database."""
    id: str = Field(..., alias="_id")


class ClienteResponse(ClienteBase):
    """Schema for Cliente response."""
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "5f9b3b3b9d9d9d9d9d9d9d9d",
                "nome": "John Doe",
                "telefone": "555-123-4567",
                "cep": "12345-678",
                "logradouro": "Rua Example",
                "numero": "123",
                "complemento": "Apt 4B",
                "cidade": "São Paulo",
                "uf": "SP",
                "instagram": "@johndoe",
                "tiktok": "@johndoe"
            }
        }