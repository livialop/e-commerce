from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Papeis
from crud.dto.schema import PapelCreate


papeis_router = APIRouter(prefix="/papeis", tags=["Papéis"])

@papeis_router.get("/papeis/", response_model=List[Papeis])
def listar_papeis(session: Session = Depends(get_session)):
    papeis = session.exec(
        select(Papeis)
    ).all()
    return papeis


@papeis_router.post("/papeis/", response_model=Papeis)
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
