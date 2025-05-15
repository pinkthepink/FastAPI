import pytest
from bson import ObjectId

from app.core.errors import NotFoundError, DuplicateError
from app.repositories.cliente_repository import ClientRepository


@pytest.mark.asyncio
async def test_find_all(client_repository: ClientRepository, sample_clients):
    """Test finding all clients."""
    # Get all clients
    clients = await client_repository.find_all()
    assert len(clients) == 3
    
    # Test skip and limit
    clients = await client_repository.find_all(skip=1, limit=1)
    assert len(clients) == 1
    
    # Test name filter
    clients = await client_repository.find_all(name="Another")
    assert len(clients) == 1
    assert clients[0]["name"] == "Another Test Client"
    
    # Test active filter
    clients = await client_repository.find_all(active=False)
    assert len(clients) == 1
    assert clients[0]["name"] == "Test Client 2"


@pytest.mark.asyncio
async def test_find_by_id(client_repository: ClientRepository, sample_clients):
    """Test finding a client by ID."""
    # Get a client by ID
    client_id = sample_clients[0]["_id"]
    client = await client_repository.find_by_id(client_id)
    assert client["name"] == "Test Client 1"
    
    # Test with string ID
    client = await client_repository.find_by_id(str(client_id))
    assert client["name"] == "Test Client 1"
    
    # Test with invalid ID
    with pytest.raises(NotFoundError):
        await client_repository.find_by_id("invalid_id")
    
    # Test with non-existent ID
    with pytest.raises(NotFoundError):
        await client_repository.find_by_id(ObjectId())


@pytest.mark.asyncio
async def test_find_by_name(client_repository: ClientRepository, sample_clients):
    """Test finding clients by name."""
    # Get clients by name
    clients = await client_repository.find_by_name("Test")
    assert len(clients) == 2
    
    # Test with non-existent name
    clients = await client_repository.find_by_name("NonExistent")
    assert len(clients) == 0


@pytest.mark.asyncio
async def test_create(client_repository: ClientRepository):
    """Test creating a client."""
    # Create a new client
    new_client_data = {
        "name": "New Test Client",
        "document_id": "444.555.666-77",
        "active": True,
        "contact": {
            "phone": "555-444-5555",
            "email": "new@example.com",
        },
        "address": {
            "street": "101 New St",
            "city": "New City",
            "state": "NC",
            "zip_code": "54321",
            "country": "New Country",
        },
    }
    
    created_client = await client_repository.create(new_client_data)
    assert created_client["name"] == "New Test Client"
    assert "_id" in created_client
    assert "created_at" in created_client
    assert "updated_at" in created_client
    
    # Test duplicate document_id
    with pytest.raises(DuplicateError):
        await client_repository.create(new_client_data)


@pytest.mark.asyncio
async def test_update(client_repository: ClientRepository, sample_clients):
    """Test updating a client."""
    client_id = sample_clients[0]["_id"]
    
    # Update a client
    update_data = {
        "name": "Updated Test Client",
        "notes": "Updated notes",
    }
    
    updated_client = await client_repository.update(client_id, update_data)
    assert updated_client["name"] == "Updated Test Client"
    assert updated_client["notes"] == "Updated notes"
    assert updated_client["document_id"] == sample_clients[0]["document_id"]
    
    # Test with invalid ID
    with pytest.raises(NotFoundError):
        await client_repository.update("invalid_id", update_data)
    
    # Test with non-existent ID
    with pytest.raises(NotFoundError):
        await client_repository.update(ObjectId(), update_data)
    
    # Test with empty update data
    with pytest.raises(ValueError):
        await client_repository.update(client_id, {})


@pytest.mark.asyncio
async def test_delete(client_repository: ClientRepository, sample_clients):
    """Test deleting a client."""
    client_id = sample_clients[0]["_id"]
    
    # Delete a client
    result = await client_repository.delete(client_id)
    assert result is True
    
    # Verify the client was deleted
    with pytest.raises(NotFoundError):
        await client_repository.find_by_id(client_id)
    
    # Test with invalid ID
    with pytest.raises(NotFoundError):
        await client_repository.delete("invalid_id")
    
    # Test with non-existent ID
    with pytest.raises(NotFoundError):
        await client_repository.delete(ObjectId())


@pytest.mark.asyncio
async def test_count(client_repository: ClientRepository, sample_clients):
    """Test counting clients."""
    # Count all clients
    count = await client_repository.count()
    assert count == 3
    
    # Test name filter
    count = await client_repository.count(name="Another")
    assert count == 1
    
    # Test active filter
    count = await client_repository.count(active=False)
    assert count == 1
    
    # Test combined filters
    count = await client_repository.count(name="Test", active=True)
    assert count == 1