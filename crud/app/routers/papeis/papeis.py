from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Papeis
from crud.dto.dto import PapelCreate, PapelUpdate


papeis_router = APIRouter(prefix="/papeis", tags=["Papéis"])

@papeis_router.get("/", response_model=List[Papeis])
def listar_papeis(session: Session = Depends(get_session)):
    papeis = session.exec(
        select(Papeis)
    ).all()
    return papeis


@papeis_router.post("/", response_model=Papeis)
def criar_papel(papel: PapelCreate, session: Session = Depends(get_session)):
    papel_existe = session.exec(
        select(Papeis).where(Papeis.nome == papel.nome)
    ).first()

    if papel_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Já existe um papel com esse nome.")
    
    novo_papel = Papeis(
        nome=papel.nome
    )

    session.add(novo_papel)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao adicionar papel.")
    
    return papel


@papeis_router.patch("/{papel_id}", response_model=Papeis)
def atualizar_papel(papel_update: PapelUpdate, papel_id: int, session: Session = Depends(get_session)):
    papel = session.get(Papeis, papel_id)
    if not papel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Papel não encontrado")

    if papel_update.nome is not None:
        papel_existente = session.exec(select(Papeis).where(Papeis.nome == papel_update.nome)).first()
        if papel_existente and papel_existente.id != papel_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Já existe um papel com esse nome.")
        papel.nome = papel_update.nome

    try:
        session.commit()
        session.refresh(papel)
        return papel
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar papel.")


@papeis_router.delete("/{papel_id}")
def deletar_papel(papel_id: int, session: Session = Depends(get_session)):
    papel = session.get(Papeis, papel_id)

    if not papel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Papel não encontrado.")

    session.delete(papel)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar papel.")