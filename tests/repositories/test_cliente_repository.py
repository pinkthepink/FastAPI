import pytest
from bson import ObjectId
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.core.errors import NotFoundError


@pytest.mark.asyncio
async def test_find_all(cliente_repository: ClienteRepository, sample_clientes):
    """Test finding all clientes."""
    # Act
    result = await cliente_repository.find_all()
    
    # Assert
    assert len(result) == 3
    assert all(cliente["_id"] for cliente in result)  # Ensure all have string IDs
    assert any(cliente["nome"] == "John Doe" for cliente in result)
    assert any(cliente["nome"] == "Jane Smith" for cliente in result)
    assert any(cliente["nome"] == "Bob Johnson" for cliente in result)


@pytest.mark.asyncio
async def test_find_by_id(cliente_repository: ClienteRepository, sample_clientes):
    """Test finding a cliente by ID."""
    # Arrange
    id = sample_clientes[0]["_id"]
    
    # Act
    result = await cliente_repository.find_by_id(id)
    
    # Assert
    assert result["_id"] == id
    assert result["nome"] == "John Doe"


@pytest.mark.asyncio
async def test_find_by_id_not_found(cliente_repository: ClienteRepository):
    """Test finding a cliente by ID when not found."""
    # Arrange
    non_existent_id = str(ObjectId())
    
    # Act & Assert
    with pytest.raises(NotFoundError) as excinfo:
        await cliente_repository.find_by_id(non_existent_id)
    
    assert "Cliente não encontrado" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create(cliente_repository: ClienteRepository):
    """Test creating a new cliente."""
    # Arrange
    new_cliente = ClienteCreate(
        nome="New Cliente",
        telefone="555-111-2222",
        cidade="Curitiba",
        uf="PR"
    )
    
    # Act
    result = await cliente_repository.create(new_cliente)
    
    # Assert
    assert result["nome"] == "New Cliente"
    assert result["telefone"] == "555-111-2222"
    assert result["cidade"] == "Curitiba"
    assert result["uf"] == "PR"
    assert "_id" in result


@pytest.mark.asyncio
async def test_update(cliente_repository: ClienteRepository, sample_clientes):
    """Test updating a cliente."""
    # Arrange
    id = sample_clientes[0]["_id"]
    update_data = ClienteUpdate(
        nome="Updated Name",
        telefone="555-999-8888"
    )
    
    # Act
    result = await cliente_repository.update(id, update_data)
    
    # Assert
    assert result["_id"] == id
    assert result["nome"] == "Updated Name"
    assert result["telefone"] == "555-999-8888"
    assert result["cidade"] == "São Paulo"  # Unchanged field


@pytest.mark.asyncio
async def test_update_not_found(cliente_repository: ClienteRepository):
    """Test updating a cliente when not found."""
    # Arrange
    non_existent_id = str(ObjectId())
    update_data = ClienteUpdate(nome="Updated Name")
    
    # Act & Assert
    with pytest.raises(NotFoundError) as excinfo:
        await cliente_repository.update(non_existent_id, update_data)
    
    assert "Cliente não encontrado" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete(cliente_repository: ClienteRepository, sample_clientes):
    """Test deleting a cliente."""
    # Arrange
    id = sample_clientes[0]["_id"]
    
    # Act
    result = await cliente_repository.delete(id)
    
    # Assert
    assert result is True
    
    # Verify it's deleted
    with pytest.raises(NotFoundError):
        await cliente_repository.find_by_id(id)


@pytest.mark.asyncio
async def test_delete_not_found(cliente_repository: ClienteRepository):
    """Test deleting a cliente when not found."""
    # Arrange
    non_existent_id = str(ObjectId())
    
    # Act & Assert
    with pytest.raises(NotFoundError) as excinfo:
        await cliente_repository.delete(non_existent_id)
    
    assert "Cliente não encontrado" in str(excinfo.value)


@pytest.mark.asyncio
async def test_find_by_nome(cliente_repository: ClienteRepository, sample_clientes):
    """Test finding clientes by nome (partial match)."""
    # Act
    result = await cliente_repository.find_by_nome("Jo")
    
    # Assert
    assert len(result) == 2  # Both John Doe and Bob Johnson
    assert any(cliente["nome"] == "John Doe" for cliente in result)
    assert any(cliente["nome"] == "Bob Johnson" for cliente in result)


@pytest.mark.asyncio
async def test_count(cliente_repository: ClienteRepository, sample_clientes):
    """Test counting total clientes."""
    # Act
    result = await cliente_repository.count()
    
    # Assert
    assert result == 3