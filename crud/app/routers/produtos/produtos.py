from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlmodel import select
from typing import List
from sqlmodel import Session

from crud.database.database import get_session
from crud.models.model import Produtos
from crud.dto.schema import ProdutoCreate


produto_router = APIRouter(prefix="/produtos", tags=["Produtos"])


@produto_router.get("/produtos/", response_model=List[Produtos])
def listar_produtos(session: Session = Depends(get_session)):
    produtos = session.exec(
        select(Produtos)
    ).all()

    return produtos

@produto_router.post("/produtos/", response_model=Produtos)
def criar_produto(produto: ProdutoCreate, session: Session = Depends(get_session)):
    if produto.preco <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Preço precisa ser maior que 0.")
    
    novo_produto: ProdutoCreate = Produtos(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco
    )    

    session.add(novo_produto)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar o produto.")
    
    return produto