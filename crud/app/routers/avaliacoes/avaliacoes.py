from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Avaliacoes
from crud.dto.dto import AvaliacaoCreate

avaliacoes_router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

@avaliacoes_router.get("/avaliacoes/", response_model=List[Avaliacoes])
def listar_avaliacoes(session: Session = Depends(get_session)):
    avaliacoes = session.exec(
        select(Avaliacoes)
    ).all()
    return avaliacoes


@avaliacoes_router.post("/avaliacoes/", response_model=Avaliacoes)
def criar_avaliacao(avaliacao: AvaliacaoCreate, session: Session = Depends(get_session)):
    usuario_existe: bool = session.exec(
        select(Avaliacoes).where(Avaliacoes.usuario_id == avaliacao.usuario_id)
    ).first()

    produto_existe: bool = session.exec(
        select(Avaliacoes).where(Avaliacoes.produto_id == avaliacao.produto_id)
    ).first()

    if not usuario_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuário não existe.")
    
    if not produto_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Produto não existe.")
    
    if avaliacao.nota < 0 or avaliacao.nota > 5:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="A nota deve ser entre 1 e 5.")
    
    nova_avaliacao: AvaliacaoCreate = Avaliacoes(
        usuario_id=avaliacao.usuario_id,
        produto_id=avaliacao.produto_id,
        nota=avaliacao.nota,
        comentario=avaliacao.comentario
    )

    session.add(nova_avaliacao)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar avaliação.")
    
    return nova_avaliacao