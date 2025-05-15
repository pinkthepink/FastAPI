from fastapi import APIRouter

from app.api.endpoints import clientes
# Temporarily comment out other imports until we implement them
# from app.api.endpoints import (
#     pets,
#     agendamentos,
#     pacotes,
#     pagamentos,
#     funcionarios,
#     servicos,
#     meios_pagamento,
#     precos_base,
#     tempos_base,
#     cadastro_rapido
# )

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
# Temporarily comment out other routers
# api_router.include_router(pets.router, prefix="/pets", tags=["pets"])
# api_router.include_router(agendamentos.router, prefix="/agendamentos", tags=["agendamentos"])
# api_router.include_router(pacotes.router, prefix="/pacotes", tags=["pacotes"])
# api_router.include_router(pagamentos.router, prefix="/pagamentos", tags=["pagamentos"])
# api_router.include_router(funcionarios.router, prefix="/funcionarios", tags=["funcionarios"])
# api_router.include_router(servicos.router, prefix="/servicos", tags=["servicos"])
# api_router.include_router(meios_pagamento.router, prefix="/meios-pagamento", tags=["meios-pagamento"])
# api_router.include_router(precos_base.router, prefix="/precos-base", tags=["precos-base"])
# api_router.include_router(tempos_base.router, prefix="/tempos-base", tags=["tempos-base"])
# api_router.include_router(cadastro_rapido.router, prefix="/agendamentos/cadastro-rapido", tags=["cadastro-rapido"])