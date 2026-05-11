from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Pagamentos
from crud.dto.dto import PagamentoCreate, PagamentoUpdate


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


@pagamentos_router.patch("/pagamentos/{pagamento_id}", response_model=Pagamentos)
def atualizar_pagamento(pagamento_update: PagamentoUpdate, pagamento_id: int, session: Session = Depends(get_session)):
    pagamento = session.get(Pagamentos, pagamento_id)
    if not pagamento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado")

    if pagamento_update.pedido_id is not None:
        pagamento.pedido_id = pagamento_update.pedido_id
    if pagamento_update.valor is not None:
        if pagamento_update.valor <= 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O valor precisa ser maior que 0.")
        pagamento.valor = pagamento_update.valor
    if pagamento_update.metodo is not None:
        pagamento.metodo = pagamento_update.metodo
    if pagamento_update.status is not None:
        pagamento.status = pagamento_update.status

    try:
        session.commit()
        session.refresh(pagamento)
        return pagamento
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar pagamento.")


@pagamentos_router.delete("/pagamentos/{pagamento_id}")
def deletar_pagamento(pagamento_id: int, session: Session = Depends(get_session)):
    pagamento = session.get(Pagamentos, pagamento_id)

    if not pagamento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado.")

    session.delete(pagamento)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar pagamento.")