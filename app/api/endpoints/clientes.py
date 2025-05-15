from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse

from app.repositories.cliente_repository import ClienteRepository
from app.api.dependencies.cliente_dependencies import get_cliente_repository
from app.utils.error_handlers import handle_api_error
from app.core.errors import NotFoundError
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter()

@router.get("/", response_model=List[ClienteResponse])
async def listar_clientes(
    repository: ClienteRepository = Depends(get_cliente_repository),
    nome: Optional[str] = Query(None, description="Filtrar por nome (parcial)")
):
    """Lista todos os clientes. Opcionalmente filtra por nome."""
    try:
        if nome:
            return await repository.find_by_nome(nome)
        return await repository.find_all()
    except Exception as e:
        error_response, status_code = handle_api_error(e, "Erro ao listar clientes")
        return JSONResponse(content=error_response, status_code=status_code)


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    cliente: ClienteCreate,
    repository: ClienteRepository = Depends(get_cliente_repository)
):
    """Cria um novo cliente."""
    try:
        return await repository.create(cliente)
    except Exception as e:
        error_response, status_code = handle_api_error(e, "Erro ao criar cliente")
        return JSONResponse(content=error_response, status_code=status_code)


@router.get("/{id}", response_model=ClienteResponse)
async def obter_cliente(
    id: str = Path(..., description="ID do cliente"),
    repository: ClienteRepository = Depends(get_cliente_repository)
):
    """Obtém um cliente pelo ID."""
    try:
        return await repository.find_by_id(id)
    except Exception as e:
        error_response, status_code = handle_api_error(e, "Erro ao buscar cliente")
        return JSONResponse(content=error_response, status_code=status_code)


@router.put("/{id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_update: ClienteUpdate,
    id: str = Path(..., description="ID do cliente"),
    repository: ClienteRepository = Depends(get_cliente_repository)
):
    """Atualiza um cliente pelo ID."""
    try:
        return await repository.update(id, cliente_update)
    except Exception as e:
        error_response, status_code = handle_api_error(e, "Erro ao atualizar cliente")
        return JSONResponse(content=error_response, status_code=status_code)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def remover_cliente(
    id: str = Path(..., description="ID do cliente"),
    repository: ClienteRepository = Depends(get_cliente_repository)
):
    """Remove um cliente pelo ID."""
    try:
        await repository.delete(id)
        return {"message": "Cliente excluído com sucesso"}
    except Exception as e:
        error_response, status_code = handle_api_error(e, "Erro ao excluir cliente")
        return JSONResponse(content=error_response, status_code=status_code)


@router.get("/count", response_model=int)
async def contar_clientes(
    repository: ClienteRepository = Depends(get_cliente_repository)
):
    """Retorna o total de clientes cadastrados."""
    try:
        return await repository.count()
    except Exception as e:
        error_response, status_code = handle_api_error(e, "Erro ao contar clientes")
        return JSONResponse(content=error_response, status_code=status_code)