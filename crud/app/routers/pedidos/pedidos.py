from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Pedidos, Usuarios
from crud.dto.dto import PedidoCreate, PedidoUpdate

pedidos_router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@pedidos_router.get("/pedidos/", response_model=List[Pedidos])
def listar_pedidos(session: Session = Depends(get_session)):
    pedidos = session.exec(
        select(Pedidos)
    ).all()
    return pedidos


@pedidos_router.post("/pedidos/", response_model=Pedidos)
def criar_pedido(pedido: PedidoCreate, session: Session = Depends(get_session)):
    usuario_existe: bool = session.exec(
        select(Usuarios).where(Usuarios.id == pedido.usuario_id)
    ).first()

    if not usuario_existe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não existe.")
    if pedido.total <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Total precisa ser maior que 0.")
    
    novo_pedido: PedidoCreate = Pedidos(
        usuario_id=pedido.usuario_id,
        total=pedido.total,
        status=pedido.status
    )

    session.add(novo_pedido)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao criar pedido.")
    
    return novo_pedido
    

@pedidos_router.patch("/pedidos/{pedido_id}", response_model=Pedidos)
def atualizar_pedido(pedido_update: PedidoUpdate, pedido_id: int, session: Session = Depends(get_session)):
    pedido = session.get(Pedidos, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")

    if pedido_update.usuario_id is not None:
        usuario_existe = session.get(Usuarios, pedido_update.usuario_id)
        if not usuario_existe:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuário não existe.")
        pedido.usuario_id = pedido_update.usuario_id
    if pedido_update.total is not None:
        if pedido_update.total <= 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Total precisa ser maior que 0.")
        pedido.total = pedido_update.total
    if pedido_update.status is not None:
        pedido.status = pedido_update.status

    try:
        session.commit()
        session.refresh(pedido)
        return pedido
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar pedido.")