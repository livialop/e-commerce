from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Usuarios, Papeis, UsuarioPapeis
from crud.dto.dto import UsuarioCreate, UsuarioUpdate

from pwdlib import PasswordHash


user_router = APIRouter(prefix="/users", tags=["Usuários"])
password_hash = PasswordHash.recommended()


@user_router.get("/", response_model=List[Usuarios])
def listar_usuarios(session: Session = Depends(get_session)):
    users = session.exec(
        select(Usuarios)
    ).all()
    return users

@user_router.post("/", response_model=Usuarios)
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

@user_router.patch("/{usuario_id}", response_model=Usuarios)
def update_user(user_update: UsuarioUpdate, usuario_id: int, session: Session = Depends(get_session)):
    user_existente = session.exec(
        select(Usuarios).where(Usuarios.id == usuario_id)
    ).first()

    usuario = session.get(Usuarios, usuario_id)

    # Checando se o usuário existe e se o email atualizado é válido
    if not user_existente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if user_update.email:
        email_utilizado = session.exec(
            select(Usuarios).where(Usuarios.email == user_update.email)
        ).first()

        if email_utilizado and user_update.email == email_utilizado.email:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="E-mail em uso.")
    

    # Fazendo o update
    if user_update.nome:
        usuario.nome = user_update.nome
    if user_update.email:
        usuario.email = user_update.email
    if user_update.senha:
        usuario.senha_hash = password_hash.hash(user_update.senha)

    try:
        session.commit()
        session.refresh(usuario)
        return usuario
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar usuário")
  
    
@user_router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuarios, usuario_id)
    
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    
    session.delete(usuario)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar usuário.")
    

# Usuários Papeis
@user_router.get("/{usuario_id}/papeis")
def listar_papeisusuarios(usuario_id: int, session: Session = Depends(get_session)):
    papeis_users = session.exec(
        select(Usuarios.nome, Papeis.nome)
        .select_from(UsuarioPapeis)
        .join(Usuarios, Usuarios.id == UsuarioPapeis.usuario_id)
        .join(Papeis, Papeis.id == UsuarioPapeis.papel_id)
        .where(UsuarioPapeis.usuario_id == usuario_id)
    ).all()

    return [
        {
            "usuario": u,
            "papel": p
        }
        for u, p in papeis_users
    ]


@user_router.post("/{usuario_id}/papeis/{papel_id}")
def criar_papelusuario(usuario_id: int, papel_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuarios, usuario_id)
    papel = session.get(Papeis, papel_id)

    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")    
    if not papel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Papel não encontrado")


    papelusuario_existe = session.exec(
        select(UsuarioPapeis).where(
            UsuarioPapeis.usuario_id == usuario_id,
            UsuarioPapeis.papel_id == papel_id
        )
    ).first()

    if papelusuario_existe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O papel desse usuário já está cadastrado.")
    
    novo_papeluser = UsuarioPapeis (
        usuario_id=usuario_id,
        papel_id=papel_id
    )

    session.add()

    try:
        session.commit()
        return novo_papeluser
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar papel ao usuário")
    
