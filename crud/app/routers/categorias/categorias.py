from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Categorias
from crud.dto.schema import CategoriaCreate


categorias_router = APIRouter(prefix="/categorias", tags=["Categorias"])

@categorias_router.get("/categorias/", response_model=List[Categorias])
def listar_categorias(session: Session = Depends(get_session)):
    categorias = session.exec(
        select(Categorias)
    ).all()
    return categorias

@categorias_router.post("/categorias/", response_model=Categorias)
def criar_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    categoria_ja_existe = session.exec(
        select(Categorias).where(Categorias.nome == categoria.nome)
    ).first()

    if categoria_ja_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Essa categoria já existe.")
    
    nova_categoria: CategoriaCreate = Categorias(
        nome=categoria.nome
    )

    session.add(nova_categoria)

    try:
        session.commit(nova_categoria)
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar categoria.")
    
    return nova_categoria