from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Pagamentos
from sqlmodel import Session

router = APIRouter()

@router.get("/pagamentos/", response_model=List[Pagamentos])
def listar_pagamentos(session: Session = Depends(get_session)):
    pagamentos = session.exec(
        select(Pagamentos)
    ).all()
    return pagamentos