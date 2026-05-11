from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Papeis
from sqlmodel import Session

router = APIRouter()

@router.get("/papeis/", response_model=List[Papeis])
def listar_papeis(session: Session = Depends(get_session)):
    papeis = session.exec(
        select(Papeis)
    ).all()
    return papeis