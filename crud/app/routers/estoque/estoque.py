from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Estoque
from crud.dto.dto import EstoqueCreate, EstoqueUpdate

estoque_router = APIRouter(prefix="/estoque", tags=["Estoque"])

@estoque_router.get("/estoque/", response_model=List[Estoque])
def listar_estoque(session: Session = Depends(get_session)):
    estoque: List[Estoque] = session.exec(
        select(Estoque)
    ).all()
    return estoque

@estoque_router.post("/estoque/", response_model=Estoque)
def criar_estoque(estoque: EstoqueCreate, session: Session = Depends(get_session)):
    produto_existe: bool = session.exec(
        select(Estoque).where(Estoque.produto_id == estoque.produto_id)
    ).first

    if produto_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Esse produto já existe.")
    if estoque.quantidade < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O estoque não pode ser negativo.")

    novo_estoque: EstoqueCreate = Estoque(
        produto_id=estoque.produto_id,
        quantidade=estoque.quantidade
    )

    session.add(novo_estoque)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar estoque.")
    
    return novo_estoque


@estoque_router.patch("/estoque/{estoque_id}", response_model=Estoque)
def atualizar_estoque(estoque_update: EstoqueUpdate, estoque_id: int, session: Session = Depends(get_session)):
    estoque = session.get(Estoque, estoque_id)
    if not estoque:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Estoque não encontrado")

    if estoque_update.produto_id is not None:
        estoque.produto_id = estoque_update.produto_id
    if estoque_update.quantidade is not None:
        if estoque_update.quantidade < 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O estoque não pode ser negativo.")
        estoque.quantidade = estoque_update.quantidade

    try:
        session.commit()
        session.refresh(estoque)
        return estoque
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar estoque.")


@estoque_router.delete("/estoque/{estoque_id}")
def deletar_estoque(estoque_id: int, session: Session = Depends(get_session)):
    estoque = session.get(Estoque, estoque_id)

    if not estoque:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Estoque não encontrado.")

    session.delete(estoque)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar estoque.")