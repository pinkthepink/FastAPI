import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import settings


@pytest.mark.asyncio
async def test_list_clients(async_client: AsyncClient, sample_clients):
    """Test listing clients."""
    response = await async_client.get(f"{settings.api_v1_str}/clients/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "total" in data
    assert "clients" in data
    assert data["total"] == 3
    assert len(data["clients"]) == 3


@pytest.mark.asyncio
async def test_list_clients_with_filtering(async_client: AsyncClient, sample_clients):
    """Test listing clients with filtering."""
    # Test name filter
    response = await async_client.get(
        f"{settings.api_v1_str}/clients/", params={"name": "Another"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["total"] == 1
    assert data["clients"][0]["name"] == "Another Test Client"
    
    # Test active filter
    response = await async_client.get(
        f"{settings.api_v1_str}/clients/", params={"active": "false"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["total"] == 1
    assert data["clients"][0]["name"] == "Test Client 2"
    
    # Test pagination
    response = await async_client.get(
        f"{settings.api_v1_str}/clients/", params={"skip": "1", "limit": "1"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["total"] == 3
    assert len(data["clients"]) == 1


@pytest.mark.asyncio
async def test_create_client(async_client: AsyncClient):
    """Test creating a client."""
    new_client_data = {
        "name": "API Test Client",
        "document_id": "999.888.777-66",
        "active": True,
        "contact": {
            "phone": "555-999-8888",
            "email": "api_test@example.com",
        },
        "address": {
            "street": "202 API St",
            "city": "API City",
            "state": "AP",
            "zip_code": "12345",
            "country": "API Country",
        },
        "notes": "API test client notes",
    }
    
    response = await async_client.post(
        f"{settings.api_v1_str}/clients/", json=new_client_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["name"] == "API Test Client"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Test duplicate document_id
    response = await async_client.post(
        f"{settings.api_v1_str}/clients/", json=new_client_data
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_get_client(async_client: AsyncClient, sample_clients):
    """Test getting a client by ID."""
    client_id = str(sample_clients[0]["_id"])
    
    response = await async_client.get(f"{settings.api_v1_str}/clients/{client_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["name"] == "Test Client 1"
    assert data["id"] == client_id
    
    # Test with invalid ID
    response = await async_client.get(f"{settings.api_v1_str}/clients/invalid_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Test with non-existent ID
    response = await async_client.get(f"{settings.api_v1_str}/clients/507f1f77bcf86cd799439011")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_client(async_client: AsyncClient, sample_clients):
    """Test updating a client."""
    client_id = str(sample_clients[0]["_id"])
    
    update_data = {
        "name": "API Updated Client",
        "notes": "Updated via API test",
    }
    
    response = await async_client.put(
        f"{settings.api_v1_str}/clients/{client_id}", json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["name"] == "API Updated Client"
    assert data["notes"] == "Updated via API test"
    assert data["document_id"] == sample_clients[0]["document_id"]
    
    # Test with invalid ID
    response = await async_client.put(
        f"{settings.api_v1_str}/clients/invalid_id", json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Test with empty update data
    response = await async_client.put(
        f"{settings.api_v1_str}/clients/{client_id}", json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_client(async_client: AsyncClient, sample_clients):
    """Test deleting a client."""
    client_id = str(sample_clients[0]["_id"])
    
    response = await async_client.delete(f"{settings.api_v1_str}/clients/{client_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify the client was deleted
    response = await async_client.get(f"{settings.api_v1_str}/clients/{client_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Test with invalid ID
    response = await async_client.delete(f"{settings.api_v1_str}/clients/invalid_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_count_clients(async_client: AsyncClient, sample_clients):
    """Test counting clients."""
    response = await async_client.get(f"{settings.api_v1_str}/clients/count")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "count" in data
    assert data["count"] == 3
    
    # Test name filter
    response = await async_client.get(
        f"{settings.api_v1_str}/clients/count", params={"name": "Another"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["count"] == 1
    
    # Test active filter
    response = await async_client.get(
        f"{settings.api_v1_str}/clients/count", params={"active": "false"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["count"] == 1
