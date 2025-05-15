import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Query, status
from fastapi.responses import JSONResponse

from app.api.dependencies.cliente_dependencies import get_client_repository
from app.core.errors import NotFoundError
from app.repositories.cliente_repository import ClientRepository
from app.schemas.cliente import (
    ClientCount,
    ClientCreate,
    ClientList,
    ClientResponse,
    ClientUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["clients"])


async def log_client_activity(activity: str, client_id: Optional[str] = None) -> None:
    """
    Background task to log client activity.
    
    Args:
        activity: The activity description
        client_id: Optional client ID related to the activity
    """
    if client_id:
        logger.info(f"Client activity: {activity} for client {client_id}")
    else:
        logger.info(f"Client activity: {activity}")


@router.get("/", response_model=ClientList, status_code=status.HTTP_200_OK)
async def list_clients(
    background_tasks: BackgroundTasks,
    repository: ClientRepository = Depends(get_client_repository),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter by client name (partial match)"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
) -> ClientList:
    """
    List clients with optional filtering.
    
    Args:
        background_tasks: FastAPI background tasks
        repository: Client repository dependency
        skip: Number of records to skip
        limit: Maximum number of records to return
        name: Filter by client name (partial match)
        active: Filter by active status
        
    Returns:
        ClientList: List of clients with total count
    """
    clients = await repository.find_all(skip=skip, limit=limit, name=name, active=active)
    total = await repository.count(name=name, active=active)
    
    background_tasks.add_task(log_client_activity, "List clients")
    
    return ClientList(total=total, clients=clients)


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client: ClientCreate,
    background_tasks: BackgroundTasks,
    repository: ClientRepository = Depends(get_client_repository),
) -> ClientResponse:
    """
    Create a new client.
    
    Args:
        client: Client data
        background_tasks: FastAPI background tasks
        repository: Client repository dependency
        
    Returns:
        ClientResponse: Created client
    """
    created_client = await repository.create(client)
    
    background_tasks.add_task(
        log_client_activity, 
        "Create client", 
        str(created_client["_id"])
    )
    
    return created_client


@router.get("/count", response_model=ClientCount, status_code=status.HTTP_200_OK)
async def count_clients(
    repository: ClientRepository = Depends(get_client_repository),
    name: Optional[str] = Query(None, description="Filter by client name (partial match)"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
) -> ClientCount:
    """
    Count clients with optional filtering.
    
    Args:
        repository: Client repository dependency
        name: Filter by client name (partial match)
        active: Filter by active status
        
    Returns:
        ClientCount: Count of clients
    """
    count = await repository.count(name=name, active=active)
    return ClientCount(count=count)


@router.get("/{client_id}", response_model=ClientResponse, status_code=status.HTTP_200_OK)
async def get_client(
    client_id: str = Path(..., description="Client ID"),
    background_tasks: BackgroundTasks = None,
    repository: ClientRepository = Depends(get_client_repository),
) -> ClientResponse:
    """
    Get a client by ID.
    
    Args:
        client_id: Client ID
        background_tasks: FastAPI background tasks
        repository: Client repository dependency
        
    Returns:
        ClientResponse: Client data
        
    Raises:
        NotFoundError: If client not found
    """
    client = await repository.find_by_id(client_id)
    
    if background_tasks:
        background_tasks.add_task(
            log_client_activity, 
            "Get client", 
            client_id
        )
    
    return client


@router.put("/{client_id}", response_model=ClientResponse, status_code=status.HTTP_200_OK)
async def update_client(
    client_update: ClientUpdate,
    client_id: str = Path(..., description="Client ID"),
    background_tasks: BackgroundTasks = None,
    repository: ClientRepository = Depends(get_client_repository),
) -> ClientResponse:
    """
    Update a client.
    
    Args:
        client_update: Client update data
        client_id: Client ID
        background_tasks: FastAPI background tasks
        repository: Client repository dependency
        
    Returns:
        ClientResponse: Updated client
        
    Raises:
        NotFoundError: If client not found
    """
    updated_client = await repository.update(client_id, client_update)
    
    if background_tasks:
        background_tasks.add_task(
            log_client_activity, 
            "Update client", 
            client_id
        )
    
    return updated_client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: str = Path(..., description="Client ID"),
    background_tasks: BackgroundTasks = None,
    repository: ClientRepository = Depends(get_client_repository),
) -> None:
    """
    Delete a client.
    
    Args:
        client_id: Client ID
        background_tasks: FastAPI background tasks
        repository: Client repository dependency
        
    Raises:
        NotFoundError: If client not found
    """
    await repository.delete(client_id)
    
    if background_tasks:
        background_tasks.add_task(
            log_client_activity, 
            "Delete client", 
            client_id
        )