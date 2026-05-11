from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from crud.database.database import get_session
from crud.models.model import Usuarios
from sqlmodel import Session

router = APIRouter()

@router.get("/users/", response_model=List[Usuarios])
def listar_usuarios(session: Session = Depends(get_session)):
    users = session.exec(
        select(Usuarios)
    ).all()
    return users

# @router.post("/users/", response_model=Usuarios)
# def create_user(session: Session = Depends(get_session)):
#     pass

# @router.patch()
# def update_user():
#     pass

