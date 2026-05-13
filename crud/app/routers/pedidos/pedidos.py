from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Pedidos, Usuarios, ItensPedido, Produtos
from crud.dto.dto import PedidoCreate, PedidoUpdate, ItemPedidoCreate
from decimal import Decimal

pedidos_router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@pedidos_router.get("/", response_model=List[Pedidos])
def listar_pedidos(session: Session = Depends(get_session)):
    pedidos = session.exec(
        select(Pedidos)
    ).all()
    return pedidos


@pedidos_router.get("/{pedido_id}/itens", response_model=List[ItensPedido])
def listar_itens_pedido(pedido_id: int, session: Session = Depends(get_session)):
    pedido = session.get(Pedidos, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

    itens = session.exec(
        select(ItensPedido).where(ItensPedido.pedido_id == pedido_id)
    ).all()

    return itens


@pedidos_router.post("/{pedido_id}/itens", response_model=ItensPedido)
def adicionar_item_pedido(pedido_id: int, item: ItemPedidoCreate, session: Session = Depends(get_session)):
    pedido = session.get(Pedidos, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

    produto = session.get(Produtos, item.produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")

    if item.quantidade <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Quantidade precisa ser maior que 0.")

    preco_unit = produto.preco
    
    novo_item = ItensPedido(
        pedido_id=pedido_id,
        produto_id=item.produto_id,
        quantidade=item.quantidade,
        preco=preco_unit
    )

    session.add(novo_item)

    if not pedido.total:
        pedido.total = (produto.preco * item.quantidade) #inicializa com o preco do produto adicionado
    pedido.total += (produto.preco * item.quantidade)

    try:
        session.commit()
        session.refresh(novo_item)
        session.refresh(pedido)
        return novo_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar item ao pedido.")



@pedidos_router.post("/", response_model=Pedidos)
def criar_pedido(pedido: PedidoCreate, session: Session = Depends(get_session)):
    usuario_existe: bool = session.exec(
        select(Usuarios).where(Usuarios.id == pedido.usuario_id)
    ).first()

    if not usuario_existe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não existe.")


    novo_pedido: PedidoCreate = Pedidos(
        usuario_id=pedido.usuario_id,
        status=pedido.status
    )

    session.add(novo_pedido)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao criar pedido.")
    
    return novo_pedido
    

@pedidos_router.patch("/{pedido_id}", response_model=Pedidos)
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


@pedidos_router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: int, session: Session = Depends(get_session)):
    pedido = session.get(Pedidos, pedido_id)

    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

    session.delete(pedido)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar pedido.")


@pedidos_router.delete("/{pedido_id}/itens/{item_id}")
def deletar_item_pedido(pedido_id: int, item_id: int, session: Session = Depends(get_session)):
    pedido = session.get(Pedidos, pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

    item = session.get(ItensPedido, item_id)
    if not item or item.pedido_id != pedido_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item do pedido não encontrado.")

    try:
        preco = item.preco
        quantidade = item.quantidade
        current_total = pedido.total if pedido.total is not None else Decimal(0)
        novo_total = current_total - (preco * quantidade)
        pedido.total = novo_total if novo_total >= 0 else Decimal(0)

        session.delete(item)
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao remover item do pedido.")