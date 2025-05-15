import asyncio
import pytest
import pytest_asyncio
import httpx
from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import AsyncGenerator, Dict, Any, List

from app.main import app as main_app
from app.database.mongodb import get_collection, mongodb, MongoDBState
from app.repositories.cliente_repository import ClienteRepository


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
    asyncio.set_event_loop(None)


@pytest.fixture
def app() -> FastAPI:
    """Get the FastAPI app."""
    return main_app


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncGenerator:
    """Get an AsyncClient instance for testing FastAPI."""
    # Create test client for FastAPI app
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def mongo_client() -> AsyncGenerator:
    """Create a MongoDB client for testing."""
    # Use a test database
    client = AsyncIOMotorClient("mongodb://localhost:27017/petshop-test")
    
    # Reset MongoDB state for tests
    mongodb_state = MongoDBState()
    mongodb_state.client = client
    mongodb_state.db = client.get_database()
    mongodb_state.collections = {}
    
    # Replace the global state with our test state
    global mongodb
    mongodb = mongodb_state
    
    # Clear the test database before each test
    db_names = await client.list_database_names()
    if "petshop-test" in db_names:
        await client.drop_database("petshop-test")
    
    yield client
    
    # Clean up after test
    await client.drop_database("petshop-test")
    client.close()


@pytest_asyncio.fixture
async def cliente_repository(mongo_client) -> ClienteRepository:
    """Get a ClienteRepository instance."""
    collection = await get_collection("clientes")
    return ClienteRepository(collection)


@pytest_asyncio.fixture
async def sample_clientes(mongo_client) -> List[Dict[str, Any]]:
    """Create sample data for clientes."""
    collection = mongodb.db.clientes
    
    sample_data = [
        {
            "nome": "John Doe",
            "telefone": "555-123-4567",
            "cidade": "São Paulo",
            "uf": "SP"
        },
        {
            "nome": "Jane Smith",
            "telefone": "555-765-4321",
            "cidade": "Rio de Janeiro",
            "uf": "RJ"
        },
        {
            "nome": "Bob Johnson",
            "telefone": "555-987-6543",
            "cidade": "Belo Horizonte",
            "uf": "MG"
        }
    ]
    
    result = await collection.insert_many(sample_data)
    
    # Get the inserted documents with their IDs
    inserted_ids = result.inserted_ids
    inserted_docs = []
    
    for i, doc_id in enumerate(inserted_ids):
        doc = sample_data[i].copy()
        doc["_id"] = str(doc_id)
        inserted_docs.append(doc)
    
    return inserted_docs