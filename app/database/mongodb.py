from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Dict, Any
from fastapi import FastAPI

from app.core.config import get_mongodb_uri, settings

# Configure logging
logger = logging.getLogger(__name__)


# MongoDB connection state management
class MongoDBState:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    collections: Dict[str, Any] = {}


# Global MongoDB state
mongodb = MongoDBState()


async def get_mongo_client() -> AsyncIOMotorClient:
    """Get MongoDB client."""
    if mongodb.client is None:
        logger.info("Creating MongoDB client...")
        mongodb.client = AsyncIOMotorClient(
            get_mongodb_uri(),
            maxPoolSize=10,
            minPoolSize=1,
            serverSelectionTimeoutMS=5000,
        )
    return mongodb.client


async def get_mongo_db() -> AsyncIOMotorDatabase:
    """Get MongoDB database."""
    if mongodb.db is None:
        client = await get_mongo_client()
        db_name = get_mongodb_uri().split("/")[-1]
        mongodb.db = client[db_name]
    return mongodb.db


async def get_collection(collection_name: str):
    """Get MongoDB collection."""
    if collection_name not in mongodb.collections:
        db = await get_mongo_db()
        mongodb.collections[collection_name] = db[collection_name]
    return mongodb.collections[collection_name]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager to handle MongoDB connections."""
    # Set up database connection
    logger.info("Connecting to MongoDB...")
    client = AsyncIOMotorClient(
        get_mongodb_uri(),
        maxPoolSize=10,
        minPoolSize=1,
        serverSelectionTimeoutMS=5000,
    )
    
    try:
        # Check connection
        await client.admin.command("ping")
        logger.info("Connected to MongoDB")
        
        # Get database name from URI
        db_name = get_mongodb_uri().split("/")[-1]
        db = client[db_name]
        
        # Store in global state
        mongodb.client = client
        mongodb.db = db
        
        # Store in app state for direct access
        app.state.db_client = client
        app.state.db = db
        
        yield  # App runs here
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    finally:
        # Close connection
        if mongodb.client:
            logger.info("Closing MongoDB connection...")
            mongodb.client.close()
            mongodb.client = None
            mongodb.db = None
            mongodb.collections = {}
            logger.info("MongoDB connection closed")