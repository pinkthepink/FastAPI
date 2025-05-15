import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from app.core.errors import NotFoundError, DatabaseError, DuplicateError
from app.schemas.cliente import ClientCreate, ClientUpdate

logger = logging.getLogger(__name__)

class ClientRepository:
    """Repository for client operations."""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def find_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find all clients with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            name: Filter by name (case-insensitive partial match)
            active: Filter by active status
            
        Returns:
            List of client dictionaries with an added 'id' field as string from _id.
        """
        query: Dict[str, Any] = {}
        
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        
        if active is not None:
            query["active"] = active
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("updated_at", -1)
        
        result = await cursor.to_list(length=limit)
        
        # Add transformation to map _id to id for each document
        for doc in result:
            doc["id"] = str(doc["_id"])
        
        return result
    
    async def find_by_id(self, id: Union[str, ObjectId]) -> Dict[str, Any]:
        """
        Find a client by ID.
        
        Args:
            id: Client ID
            
        Returns:
            Client dictionary
            
        Raises:
            NotFoundError: If client not found
        """
        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except Exception as e:
                logger.error(f"Invalid ObjectId format: {id}, error: {e}")
                raise NotFoundError(f"Invalid client ID format: {id}")
        
        client = await self.collection.find_one({"_id": id})
        
        if not client:
            raise NotFoundError(f"Client with ID {id} not found")
        
        # Add id field
        client["id"] = str(client["_id"])
        
        return client
    
    async def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Find clients by name (case-insensitive partial match).
        
        Args:
            name: Client name to search for
            
        Returns:
            List of matching client dictionaries
        """
        cursor = self.collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        ).sort("name", 1)
        
        result = await cursor.to_list(length=100)
        
        # Add id field for each document
        for doc in result:
            doc["id"] = str(doc["_id"])
            
        return result
    
    async def create(self, client_data: Union[ClientCreate, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new client.
        
        Args:
            client_data: Client data to insert
            
        Returns:
            Created client dictionary
            
        Raises:
            DuplicateError: If client with same document_id already exists
            DatabaseError: If database operation fails
        """
        if isinstance(client_data, ClientCreate):
            client_data = client_data.model_dump()
        
        # Check if document_id already exists to provide better error message
        existing = await self.collection.find_one({"document_id": client_data["document_id"]})
        if existing:
            raise DuplicateError(f"Client with document_id {client_data['document_id']} already exists")
        
        # Use datetime.now(timezone.utc) instead of datetime.utcnow()
        from datetime import timezone
        now = datetime.now(timezone.utc)
        client_dict = {
            **client_data,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await self.collection.insert_one(client_dict)
            if not result.inserted_id:
                raise DatabaseError("Failed to insert client")
            
            return await self.find_by_id(result.inserted_id)
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error: {e}")
            raise DuplicateError(f"Client with duplicate key already exists: {e}")
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Error creating client: {e}")
    
    async def update(
        self, id: Union[str, ObjectId], update_data: Union[ClientUpdate, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update a client.
        
        Args:
            id: Client ID
            update_data: Data to update
            
        Returns:
            Updated client dictionary
            
        Raises:
            NotFoundError: If client not found
            DatabaseError: If database operation fails
        """
        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except Exception as e:
                logger.error(f"Invalid ObjectId format: {id}, error: {e}")
                raise NotFoundError(f"Invalid client ID format: {id}")
        
        if isinstance(update_data, ClientUpdate):
            # Filter out None values
            update_data = {k: v for k, v in update_data.model_dump().items() if v is not None}
        
        if not update_data:
            raise ValueError("No update data provided")
        
        # Check if client exists
        await self.find_by_id(id)
        
        # Use datetime.now(timezone.utc) instead of datetime.utcnow()
        from datetime import timezone
        update_dict = {
            "$set": {
                **update_data,
                "updated_at": datetime.now(timezone.utc),
            }
        }
        
        try:
            result = await self.collection.update_one({"_id": id}, update_dict)
            
            if result.matched_count == 0:
                raise NotFoundError(f"Client with ID {id} not found")
            
            if result.modified_count == 0:
                logger.warning(f"Client {id} was not modified by update")
            
            return await self.find_by_id(id)
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error: {e}")
            raise DuplicateError(f"Update would create a duplicate client: {e}")
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Error updating client: {e}")
    
    async def delete(self, id: Union[str, ObjectId]) -> bool:
        """
        Delete a client.
        
        Args:
            id: Client ID
            
        Returns:
            True if client was deleted
            
        Raises:
            NotFoundError: If client not found
            DatabaseError: If database operation fails
        """
        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except Exception as e:
                logger.error(f"Invalid ObjectId format: {id}, error: {e}")
                raise NotFoundError(f"Invalid client ID format: {id}")
        
        # Check if client exists
        await self.find_by_id(id)
        
        try:
            result = await self.collection.delete_one({"_id": id})
            
            if result.deleted_count == 0:
                raise NotFoundError(f"Client with ID {id} not found or not deleted")
            
            return True
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Error deleting client: {e}")
    
    async def count(self, name: Optional[str] = None, active: Optional[bool] = None) -> int:
        """
        Count clients with optional filtering.
        
        Args:
            name: Filter by name (case-insensitive partial match)
            active: Filter by active status
            
        Returns:
            Count of matching clients
        """
        query: Dict[str, Any] = {}
        
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        
        if active is not None:
            query["active"] = active
        
        try:
            count = await self.collection.count_documents(query)
            return count
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Error counting clients: {e}")