from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlmodel import select
from typing import List
from sqlmodel import Session

from crud.database.database import get_session
from crud.models.model import Produtos, ProdutoCategorias, Categorias
from crud.dto.dto import ProdutoCreate, ProdutoUpdate, ProdutoCategoriaUpdate


produto_router = APIRouter(prefix="/produtos", tags=["Produtos"])


@produto_router.get("/", response_model=List[Produtos])
def listar_produtos(session: Session = Depends(get_session)):
    produtos = session.exec(
        select(Produtos)
    ).all()

    return produtos

@produto_router.post("/", response_model=Produtos)
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


@produto_router.patch("/{produto_id}", response_model=Produtos)
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


@produto_router.delete("/{produto_id}")
def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
    produto = session.get(Produtos, produto_id)
    
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")
    
    session.delete(produto)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar produto.")
    

# Produtos Categorias
@produto_router.get("/{produto_id}/categoria")
def listar_produtos_categorias(produto_id: int, session: Session = Depends(get_session)):
    produtos_categorias = session.exec(
        select(Produtos.nome, Categorias.nome)
        .select_from(ProdutoCategorias)
        .join(Produtos, Produtos.id == ProdutoCategorias.produto_id)
        .join(Categorias, Categorias.id == ProdutoCategorias.categoria_id)
        .where(ProdutoCategorias.produto_id == produto_id)
    ).all()

    return [
        {
            "produto": p,
            "categoria": c
        } for p, c in produtos_categorias
    ]


@produto_router.post("/{produto_id}/categorias/{categoria_id}")
def criar_categoria_prod(produto_id: int, categoria_id: int, session: Session = Depends(get_session)):
    produto = session.get(Produtos, produto_id)
    categoria = session.get(Categorias, categoria_id)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")
    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")    
    
    existe = session.exec(
        select(ProdutoCategorias)
        .where(ProdutoCategorias.categoria_id == categoria_id, ProdutoCategorias.produto_id == produto_id)
    ).first()

    if existe:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Já existe produto com essa categoria")
    
    nova_cat_prod = ProdutoCategorias(
        produto_id=produto_id,
        categoria_id=categoria_id
    )

    session.add()

    try:
        session.commit()
        return nova_cat_prod
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar a categoria do produto.")
    
@produto_router.patch("/{produto_id}/categorias/{categoria_id}")
def atualizar_categoria_prod(catprod_update: ProdutoCategoriaUpdate, produto_id: int, categoria_id: int, session: Session = Depends(get_session)):
    prod_categoria = session.get(ProdutoCategoriaUpdate, (produto_id, categoria_id))
    produto = session.get(Produtos, produto_id)
    categoria = session.get(Categorias, categoria_id)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")

    if catprod_update.produto_id != produto.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Não pode trocar o produto.")

    categoria_existe = session.exec(
        select(Categorias.id)
    ).all()


    if catprod_update.categoria_id in categoria_existe:
        if catprod_update.categoria_id != prod_categoria.categoria_id:
            prod_categoria.categoria_id = catprod_update.categoria_id
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Esse produto já está com essa categoria.")
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Essa categoria não existe.")

    try:
        session.commit()
        session.refresh(prod_categoria)
        return prod_categoria
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar categoria do produto")