from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Estoque
from sqlmodel import Session

router = APIRouter()

@router.get("/estoque/", response_model=List[Estoque])
def listar_estoque(session: Session = Depends(get_session)):
    estoque = session.exec(
        select(Estoque)
    ).all()
    return estoque