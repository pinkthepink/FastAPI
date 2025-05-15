from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class ClientBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive on client creation
class ClientCreate(ClientBase):
    name: str
    email: EmailStr


# Properties to receive on client update
class ClientUpdate(ClientBase):
    pass


# Properties shared by models stored in DB
class ClientInDBBase(ClientBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# Properties to return to client
class Client(ClientInDBBase):
    pass


# Properties properties stored in DB
class ClientInDB(ClientInDBBase):
    pass