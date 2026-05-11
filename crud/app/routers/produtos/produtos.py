from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Produtos
from sqlmodel import Session

router = APIRouter()

@router.get("/produtos/", response_model=List[Produtos])
def listar_produtos(session: Session = Depends(get_session)):
    produtos = session.exec(
        select(Produtos)
    ).all()

    return produtos