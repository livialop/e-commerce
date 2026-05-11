from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Pagamentos
from crud.dto.dto import PagamentoCreate


pagamentos_router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@pagamentos_router.get("/pagamentos/", response_model=List[Pagamentos])
def listar_pagamentos(session: Session = Depends(get_session)):
    pagamentos = session.exec(
        select(Pagamentos)
    ).all()
    return pagamentos

@pagamentos_router.post("/pagamentos/", response_model=Pagamentos)
def criar_pagamento(pagamento: PagamentoCreate, session: Session = Depends(get_session)):
    if pagamento.valor <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O valor precisa ser maior que 0.")
    
    novo_pagamento: PagamentoCreate = Pagamentos(
        pedido_id=pagamento.pedido_id,
        valor=pagamento.valor,
        metodo=pagamento.metodo,
        status=pagamento.status
    )

    session.add(novo_pagamento)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar pagamento.")
    
    return novo_pagamento