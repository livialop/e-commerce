from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Enderecos
from sqlmodel import Session

router = APIRouter()

@router.get("/enderecos/", response_model=List[Enderecos])
def listar_enderecos(session: Session = Depends(get_session)):
    enderecos = session.exec(
        select(Enderecos)
    ).all()
    return enderecos