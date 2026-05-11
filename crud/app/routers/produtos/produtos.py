from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlmodel import select
from typing import List
from sqlmodel import Session

from crud.database.database import get_session
from crud.models.model import Produtos
from crud.dto.dto import ProdutoCreate, ProdutoUpdate


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


@produto_router.patch("/produtos/{produto_id}", response_model=Produtos)
def atualizar_produto(produto_update: ProdutoUpdate, produto_id: int, session: Session = Depends(get_session)):
    produto = session.get(Produtos, produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    if produto_update.nome is not None:
        produto.nome = produto_update.nome
    if produto_update.descricao is not None:
        produto.descricao = produto_update.descricao
    if produto_update.preco is not None:
        if produto_update.preco <= 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Preço precisa ser maior que 0.")
        produto.preco = produto_update.preco

    try:
        session.commit()
        session.refresh(produto)
        return produto
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar produto.")