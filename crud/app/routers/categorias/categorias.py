from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Categorias
from sqlmodel import Session

router = APIRouter()

@router.get("/categorias/", response_model=List[Categorias])
def listar_categorias(session: Session = Depends(get_session)):
    categorias = session.exec(
        select(Categorias)
    ).all()
    return categorias