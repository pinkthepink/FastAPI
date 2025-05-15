import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError

from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

mongodb = MongoDB()

async def connect_to_mongo() -> None:
    """Create database connection."""
    logger.info("Connecting to MongoDB...")
    try:
        mongodb.client = AsyncIOMotorClient(
            settings.mongodb_uri,
            maxPoolSize=10,
            minPoolSize=1,
            serverSelectionTimeoutMS=5000,
        )
        
        # Validate connection
        await mongodb.client.admin.command("ping")
        logger.info("Connected to MongoDB")
        
        mongodb.db = mongodb.client[settings.mongodb_db_name]
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection() -> None:
    """Close database connection."""
    logger.info("Closing MongoDB connection...")
    if mongodb.client:
        mongodb.client.close()
        mongodb.client = None
        mongodb.db = None
    logger.info("MongoDB connection closed")

@asynccontextmanager
async def lifespan(app):
    """FastAPI lifespan context manager for database connection."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()

def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    """Get MongoDB collection."""
    if not mongodb.db:
        raise ConnectionError("MongoDB connection not established")
    return mongodb.db[collection_name]

async def create_indexes() -> None:
    """Create indexes for MongoDB collections."""
    if not mongodb.db:
        raise ConnectionError("MongoDB connection not established")
    
    # Create indexes for the client collection
    client_collection = get_collection("clients")
    await client_collection.create_index("email", unique=True)
    await client_collection.create_index("name")
    
    logger.info("MongoDB indexes created successfully")