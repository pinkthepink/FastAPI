from typing import List, Optional, Dict, Any
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from pymongo.collection import Collection

from app.core.errors import NotFoundError, DatabaseError
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse


class ClienteRepository:
    """Repository for Cliente operations."""
    
    def __init__(self, collection: Collection):
        self.collection = collection
    
    async def find_all(self) -> List[Dict[str, Any]]:
        """Find all clientes."""
        try:
            clientes = await self.collection.find().to_list(None)
            # Convert ObjectId to str
            for cliente in clientes:
                cliente["_id"] = str(cliente["_id"])
            return clientes
        except Exception as e:
            raise DatabaseError(f"Error finding clientes: {str(e)}")
    
    async def find_by_id(self, id: str) -> Dict[str, Any]:
        """Find a cliente by ID."""
        try:
            try:
                obj_id = ObjectId(id)
            except InvalidId:
                raise NotFoundError("Cliente")
                
            cliente = await self.collection.find_one({"_id": obj_id})
            
            if not cliente:
                raise NotFoundError("Cliente")
                
            # Convert ObjectId to str
            cliente["_id"] = str(cliente["_id"])
            
            return cliente
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Error finding cliente: {str(e)}")
    
    async def create(self, cliente: ClienteCreate) -> Dict[str, Any]:
        """Create a new cliente."""
        try:
            # Insert the new cliente
            result = await self.collection.insert_one(cliente.model_dump(exclude_unset=True))
            
            # Fetch the created cliente
            created_cliente = await self.collection.find_one({"_id": result.inserted_id})
            
            # Convert ObjectId to str
            created_cliente["_id"] = str(created_cliente["_id"])
            
            return created_cliente
        except Exception as e:
            raise DatabaseError(f"Error creating cliente: {str(e)}")
    
    async def update(self, id: str, cliente: ClienteUpdate) -> Dict[str, Any]:
        """Update a cliente."""
        try:
            try:
                obj_id = ObjectId(id)
            except InvalidId:
                raise NotFoundError("Cliente")
                
            # Filter out None values to avoid overwriting with None
            update_data = {k: v for k, v in cliente.model_dump(exclude_unset=True).items() if v is not None}
            
            # Update the cliente
            result = await self.collection.find_one_and_update(
                {"_id": obj_id},
                {"$set": update_data},
                return_document=True
            )
            
            if not result:
                raise NotFoundError("Cliente")
                
            # Convert ObjectId to str
            result["_id"] = str(result["_id"])
            
            return result
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Error updating cliente: {str(e)}")
    
    async def delete(self, id: str) -> bool:
        """Delete a cliente."""
        try:
            try:
                obj_id = ObjectId(id)
            except InvalidId:
                raise NotFoundError("Cliente")
                
            result = await self.collection.delete_one({"_id": obj_id})
            
            if result.deleted_count == 0:
                raise NotFoundError("Cliente")
                
            return True
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Error deleting cliente: {str(e)}")
    
    async def find_by_nome(self, nome: str) -> List[Dict[str, Any]]:
        """Find clientes by nome (partial match)."""
        try:
            clientes = await self.collection.find(
                {"nome": {"$regex": nome, "$options": "i"}}  # Case-insensitive search
            ).to_list(None)
            
            # Convert ObjectId to str
            for cliente in clientes:
                cliente["_id"] = str(cliente["_id"])
                
            return clientes
        except Exception as e:
            raise DatabaseError(f"Error finding clientes by nome: {str(e)}")
    
    async def count(self) -> int:
        """Count total clientes."""
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            raise DatabaseError(f"Error counting clientes: {str(e)}")