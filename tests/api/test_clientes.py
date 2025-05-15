import pytest
from httpx import AsyncClient
from bson import ObjectId
import json

from app.main import app


# Helper function to convert ObjectId to string in JSON
def json_dumps(data):
    return json.dumps(data, default=str)


@pytest.mark.asyncio
async def test_list_clientes(async_client: AsyncClient, sample_clientes):
    """Test listing all clientes."""
    # Act
    response = await async_client.get("/api/clientes/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    # The database has existing data, just check our test data is included
    assert any(cliente["nome"] == "John Doe" for cliente in data)
    assert any(cliente["nome"] == "Jane Smith" for cliente in data)
    assert any(cliente["nome"] == "Bob Johnson" for cliente in data)



@pytest.mark.asyncio
async def test_get_cliente(async_client: AsyncClient, sample_clientes):
    """Test getting a cliente by ID."""
    # Arrange
    id = sample_clientes[0]["_id"]
    
    # Act
    response = await async_client.get(f"/api/clientes/{id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == id
    assert data["nome"] == "John Doe"


@pytest.mark.asyncio
async def test_get_cliente_not_found(async_client: AsyncClient):
    """Test getting a cliente by ID when not found."""
    # Arrange
    non_existent_id = str(ObjectId())
    
    # Act
    response = await async_client.get(f"/api/clientes/{non_existent_id}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "Cliente não encontrado" in data["error"]


@pytest.mark.asyncio
async def test_create_cliente(async_client: AsyncClient):
    """Test creating a new cliente."""
    # Arrange
    new_cliente = {
        "nome": "New Cliente",
        "telefone": "555-111-2222",
        "cidade": "Curitiba",
        "uf": "PR"
    }
    
    # Act
    response = await async_client.post("/api/clientes/", json=new_cliente)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "New Cliente"
    assert data["telefone"] == "555-111-2222"
    assert data["cidade"] == "Curitiba"
    assert data["uf"] == "PR"
    assert "_id" in data


@pytest.mark.asyncio
async def test_create_cliente_invalid(async_client: AsyncClient):
    """Test creating a new cliente with invalid data."""
    # Arrange
    invalid_cliente = {
        # Missing required nome field
        "telefone": "555-111-2222"
    }
    
    # Act
    response = await async_client.post("/api/clientes/", json=invalid_cliente)
    
    # Assert
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_update_cliente(async_client: AsyncClient, sample_clientes):
    """Test updating a cliente."""
    # Arrange
    id = sample_clientes[0]["_id"]
    update_data = {
        "nome": "Updated Name",
        "telefone": "555-999-8888"
    }
    
    # Act
    response = await async_client.put(f"/api/clientes/{id}", json=update_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == id
    assert data["nome"] == "Updated Name"
    assert data["telefone"] == "555-999-8888"
    assert data["cidade"] == "São Paulo"  # Unchanged field


@pytest.mark.asyncio
async def test_update_cliente_not_found(async_client: AsyncClient):
    """Test updating a cliente when not found."""
    # Arrange
    non_existent_id = str(ObjectId())
    update_data = {"nome": "Updated Name"}
    
    # Act
    response = await async_client.put(f"/api/clientes/{non_existent_id}", json=update_data)
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "Cliente não encontrado" in data["error"]


@pytest.mark.asyncio
async def test_delete_cliente(async_client: AsyncClient, sample_clientes):
    """Test deleting a cliente."""
    # Arrange
    id = sample_clientes[0]["_id"]
    
    # Act
    response = await async_client.delete(f"/api/clientes/{id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Cliente excluído com sucesso"
    
    # Verify it's deleted
    get_response = await async_client.get(f"/api/clientes/{id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_cliente_not_found(async_client: AsyncClient):
    """Test deleting a cliente when not found."""
    # Arrange
    non_existent_id = str(ObjectId())
    
    # Act
    response = await async_client.delete(f"/api/clientes/{non_existent_id}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "Cliente não encontrado" in data["error"]


@pytest.mark.asyncio
async def test_filter_clientes_by_nome(async_client: AsyncClient, sample_clientes):
    """Test filtering clientes by nome."""
    # Act
    response = await async_client.get("/api/clientes/?nome=Jo")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Both John Doe and Bob Johnson
    assert any(cliente["nome"] == "John Doe" for cliente in data)
    assert any(cliente["nome"] == "Bob Johnson" for cliente in data)