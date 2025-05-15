from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Client])
async def read_clients(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve clients.
    """
    if crud.user.is_superuser(current_user):
        clients = await crud.client.get_multi(db, skip=skip, limit=limit)
    else:
        clients = await crud.client.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return clients


@router.post("/", response_model=schemas.Client)
async def create_client(
    *,
    db: AsyncSession = Depends(deps.get_db),
    client_in: schemas.ClientCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new client.
    """
    client = await crud.client.get_by_email(db=db, email=client_in.email)
    if client:
        raise HTTPException(
            status_code=400,
            detail="A client with this email already exists in the system.",
        )
    client = await crud.client.create(db=db, obj_in=client_in, created_by=current_user.id)
    return client


@router.get("/{client_id}", response_model=schemas.Client)
async def read_client(
    *,
    db: AsyncSession = Depends(deps.get_db),
    client_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get client by ID.
    """
    client = await crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if not crud.user.is_superuser(current_user) and (client.created_by != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return client


@router.put("/{client_id}", response_model=schemas.Client)
async def update_client(
    *,
    db: AsyncSession = Depends(deps.get_db),
    client_id: int,
    client_in: schemas.ClientUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a client.
    """
    client = await crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if not crud.user.is_superuser(current_user) and (client.created_by != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    client = await crud.client.update(db=db, db_obj=client, obj_in=client_in)
    return client


@router.delete("/{client_id}", response_model=schemas.Client)
async def delete_client(
    *,
    db: AsyncSession = Depends(deps.get_db),
    client_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a client.
    """
    client = await crud.client.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if not crud.user.is_superuser(current_user) and (client.created_by != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    client = await crud.client.remove(db=db, id=client_id)
    return client