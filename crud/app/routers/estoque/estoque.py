from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Estoque
from crud.dto.schema import EstoqueCreate

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