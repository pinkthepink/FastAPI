from fastapi import Depends
from pymongo.collection import Collection

from app.database.mongodb import get_collection
from app.repositories.cliente_repository import ClienteRepository


async def get_cliente_collection() -> Collection:
    """Get the Cliente collection."""
    return await get_collection("clientes")


async def get_cliente_repository(collection: Collection = Depends(get_cliente_collection)) -> ClienteRepository:
    """Get the Cliente repository."""
    return ClienteRepository(collection)