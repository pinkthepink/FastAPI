import asyncio
import os
from typing import AsyncGenerator, Generator, List

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.api_router import api_router
from app.core.config import settings
from app.database.mongodb import MongoDB, get_collection
from app.repositories.cliente_repository import ClientRepository
from app.utils.error_handlers import setup_error_handlers


# Use a test database
TEST_MONGODB_URI = os.environ.get("TEST_MONGODB_URI", "mongodb://localhost:27017")
TEST_MONGODB_DB_NAME = f"test_{settings.mongodb_db_name}"


# Override settings for testing
settings.mongodb_uri = TEST_MONGODB_URI
settings.mongodb_db_name = TEST_MONGODB_DB_NAME


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    """Create a MongoDB client for testing."""
    import sys
    # Initialize MongoDB client
    client = AsyncIOMotorClient(
        TEST_MONGODB_URI,
        maxPoolSize=10,
        minPoolSize=1,
        serverSelectionTimeoutMS=5000,
    )
    
    # Check if MongoDB is actually running
    try:
        # Ping the MongoDB server
        await client.admin.command("ping")
        
        # Set the test MongoDB client and database
        mongodb = MongoDB()
        mongodb.client = client
        mongodb.db = client[TEST_MONGODB_DB_NAME]
        
        yield client
        
        # Clean up database after tests
        await client.drop_database(TEST_MONGODB_DB_NAME)
        client.close()
    except Exception as e:
        print(f"\nERROR: Could not connect to MongoDB: {e}")
        print("Is MongoDB running on your system?")
        print("For running tests, you need MongoDB installed and running.")
        print("Alternative: use pytest with --skip-mongo flag to skip tests requiring MongoDB.\n")
        sys.exit(1)


@pytest_asyncio.fixture(scope="function")
async def clean_test_db(mongo_client) -> None:
    """Clean the test database before each test."""
    await mongo_client.drop_database(TEST_MONGODB_DB_NAME)


@pytest_asyncio.fixture
async def app(mongo_client) -> FastAPI:
    """Create a FastAPI test application."""
    app = FastAPI()
    setup_error_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_str)
    return app


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    async with AsyncClient(base_url="http://test") as client:
        app_client = TestClient(app)
        transport = ASGITransport(app=app)
        client.transport = transport
        yield client


@pytest_asyncio.fixture
async def client_repository(mongo_client, clean_test_db) -> ClientRepository:
    """Create a client repository for testing."""
    # Make sure MongoDB client is set in global MongoDB object
    from app.database.mongodb import mongodb
    if not mongodb.db:
        mongodb.client = mongo_client
        mongodb.db = mongo_client[TEST_MONGODB_DB_NAME]
        
    collection = get_collection("clients")
    return ClientRepository(collection)


@pytest_asyncio.fixture
async def sample_clients(client_repository: ClientRepository) -> List[dict]:
    """Create sample clients for testing."""
    sample_data = [
        {
            "name": "Test Client 1",
            "document_id": "123.456.789-00",
            "active": True,
            "contact": {
                "phone": "555-123-4567",
                "email": "client1@example.com",
            },
            "address": {
                "street": "123 Main St",
                "city": "Test City",
                "state": "TS",
                "zip_code": "12345",
                "country": "Test Country",
            },
            "notes": "Test client 1 notes",
        },
        {
            "name": "Test Client 2",
            "document_id": "987.654.321-00",
            "active": False,
            "contact": {
                "phone": "555-987-6543",
                "email": "client2@example.com",
                "alternative_phone": "555-111-2222",
            },
            "address": {
                "street": "456 Oak Ave",
                "city": "Sample City",
                "state": "SC",
                "zip_code": "54321",
                "country": "Sample Country",
            },
        },
        {
            "name": "Another Test Client",
            "document_id": "111.222.333-44",
            "active": True,
            "contact": {
                "phone": "555-333-4444",
                "email": "another@example.com",
            },
            "address": {
                "street": "789 Pine Rd",
                "city": "Another City",
                "state": "AC",
                "zip_code": "67890",
                "country": "Another Country",
            },
            "notes": "Another test client notes",
        },
    ]
    
    created_clients = []
    for client_data in sample_data:
        created = await client_repository.create(client_data)
        created_clients.append(created)
    
    return created_clients