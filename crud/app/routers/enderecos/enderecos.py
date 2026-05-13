from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Enderecos
from crud.dto.dto import EnderecoCreate, EnderecoUpdate

enderecos_router = APIRouter(prefix="/enderecos", tags=["Endereços"])

@enderecos_router.get("/", response_model=List[Enderecos])
def listar_enderecos(session: Session = Depends(get_session)):
    enderecos = session.exec(
        select(Enderecos)
    ).all()
    return enderecos

@enderecos_router.post("/", response_model=Enderecos)
def criar_endereco(endereco: EnderecoCreate, session: Session = Depends(get_session)):
    endereco_ja_cadastrado: bool = session.exec(
        select(Enderecos).where(Enderecos.usuario_id == endereco.usuario_id)
    ).first()

    if endereco_ja_cadastrado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O usuário já possui um endereço cadastrado.")
    
    novo_endereco: EnderecoCreate = Enderecos(
        usuario_id=endereco.usuario_id,
        rua=endereco.rua,
        cidade=endereco.cidade,
        estado=endereco.estado,
        cep=endereco.cep
    )

    session.add(novo_endereco)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao registrar endereço.")
    
    return novo_endereco


@enderecos_router.patch("/{endereco_id}", response_model=Enderecos)
def atualizar_endereco(endereco_update: EnderecoUpdate, endereco_id: int, session: Session = Depends(get_session)):
    endereco = session.get(Enderecos, endereco_id)
    if not endereco:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado")

    if endereco_update.usuario_id is not None:
        endereco.usuario_id = endereco_update.usuario_id
    if endereco_update.rua is not None:
        endereco.rua = endereco_update.rua
    if endereco_update.cidade is not None:
        endereco.cidade = endereco_update.cidade
    if endereco_update.estado is not None:
        endereco.estado = endereco_update.estado
    if endereco_update.cep is not None:
        endereco.cep = endereco_update.cep

    try:
        session.commit()
        session.refresh(endereco)
        return endereco
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao atualizar endereço.")


@enderecos_router.delete("/{endereco_id}")
def deletar_endereco(endereco_id: int, session: Session = Depends(get_session)):
    endereco = session.get(Enderecos, endereco_id)

    if not endereco:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado.")

    session.delete(endereco)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao deletar endereço.")