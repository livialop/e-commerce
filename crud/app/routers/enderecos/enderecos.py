from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List

from crud.database.database import get_session
from crud.models.model import Enderecos
from crud.dto.schema import EnderecoCreate

enderecos_router = APIRouter(prefix="/enderecos", tags=["Endereços"])

@enderecos_router.get("/enderecos/", response_model=List[Enderecos])
def listar_enderecos(session: Session = Depends(get_session)):
    enderecos = session.exec(
        select(Enderecos)
    ).all()
    return enderecos

@enderecos_router.post("/enderecos/", response_model=Enderecos)
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
