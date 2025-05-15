from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_collection
from app.repositories.cliente_repository import ClientRepository


async def get_client_collection() -> AsyncIOMotorCollection:
    """
    Get the clients collection from the database.
    
    Returns:
        AsyncIOMotorCollection: The clients collection
    """
    return get_collection("clients")


async def get_client_repository(
    collection: AsyncIOMotorCollection = Depends(get_client_collection),
) -> ClientRepository:
    """
    Get the client repository instance.
    
    Args:
        collection: The clients collection dependency
        
    Returns:
        ClientRepository: The client repository instance
    """
    return ClientRepository(collection)