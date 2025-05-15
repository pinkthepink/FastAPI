from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

# Use PyObjectId as a converter/validator for MongoDB ObjectId strings
PyObjectId = Annotated[str, BeforeValidator(str)]


class Address(BaseModel):
    """Client address schema."""
    
    street: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    zip_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=50)
    

class Contact(BaseModel):
    """Client contact information schema."""
    
    phone: str = Field(..., min_length=5, max_length=20, examples=["555-123-4567"])
    email: EmailStr
    alternative_phone: Optional[str] = Field(None, min_length=5, max_length=20, examples=["555-987-6543"])
    

class ClientBase(BaseModel):
    """Base client schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=100)
    document_id: str = Field(..., min_length=5, max_length=20, examples=["123.456.789-00"])
    active: bool = True
    contact: Contact
    address: Address
    notes: Optional[str] = None
    

class ClientCreate(ClientBase):
    """Schema for client creation."""
    pass


class ClientUpdate(BaseModel):
    """Schema for client update (all fields optional)."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    document_id: Optional[str] = Field(None, min_length=5, max_length=20, examples=["123.456.789-00"])
    active: Optional[bool] = None
    contact: Optional[Contact] = None
    address: Optional[Address] = None
    notes: Optional[str] = None
    
    @field_validator('*')
    @classmethod
    def check_empty_update(cls, values):
        """Validate that at least one field is being updated."""
        if all(v is None for v in values.values()):
            raise ValueError("At least one field must be provided for update")
        return values


class ClientInDB(ClientBase):
    """Schema for client as stored in database."""
    
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    updated_at: datetime


class ClientResponse(ClientBase):
    """Schema for client API responses."""
    
    id: PyObjectId
    created_at: datetime
    updated_at: datetime


class ClientList(BaseModel):
    """Schema for returning multiple clients."""
    
    total: int
    clients: List[ClientResponse]
    

class ClientCount(BaseModel):
    """Schema for client count response."""
    
    count: int