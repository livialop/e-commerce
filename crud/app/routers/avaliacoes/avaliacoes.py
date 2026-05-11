from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Avaliacoes
from sqlmodel import Session

router = APIRouter()

@router.get("/avaliacoes/", response_model=List[Avaliacoes])
def listar_avaliacoes(session: Session = Depends(get_session)):
    avaliacoes = session.exec(
        select(Avaliacoes)
    ).all()
    return avaliacoes
