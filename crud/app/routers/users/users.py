from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Usuarios
from crud.dto.dto import UsuarioCreate

from pwdlib import PasswordHash


user_router = APIRouter(prefix="/users", tags=["Usuários"])
password_hash = PasswordHash.recommended()


@user_router.get("/users/", response_model=List[Usuarios])
def listar_usuarios(session: Session = Depends(get_session)):
    users = session.exec(
        select(Usuarios)
    ).all()
    return users

@user_router.post("/users/", response_model=Usuarios)
def criar_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    usuario_existe: bool = session.exec(
        select(Usuarios).where(Usuarios.email == usuario.email)
    ).first()

    if usuario_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado.")
    
    novo_user: UsuarioCreate = Usuarios(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=password_hash.hash(usuario.senha)
    )

    session.add(novo_user)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Falha ao criar usuário")
    
    return novo_user

# @router.patch()
# def update_user():
#     pass

