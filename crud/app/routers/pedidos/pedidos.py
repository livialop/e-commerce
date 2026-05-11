from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Pedidos
from sqlmodel import Session

router = APIRouter()

@router.get("/pedidos/", response_model=List[Pedidos])
def listar_pedidos(session: Session = Depends(get_session)):
    pedidos = session.exec(
        select(Pedidos)
    ).all()
    return pedidos