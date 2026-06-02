from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel import select, Session

from crud.models.model import Usuarios
from crud.database.database import get_session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from pwdlib import PasswordHash
from typing import Annotated
from tokenize import Token
from datetime import datetime, timedelta
import jwt


token_schema = OAuth2PasswordBearer(tokenUrl="token")
login_router = APIRouter(prefix="/auth", tags=["Auth"])
password_hash = PasswordHash.recommended()
SECRET_KEY = 'KJASDKAJDWUHAsajdkaj' # so pra teste, dps vai pro .env
ALGORITMO = 'HS256' # teste, dps vai pro .env

def create_access_token(data: dict):
    to_encode = data.copy() # o data seria o sub -> email do usuario
    expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITMO
    )
    return token

def get_usuario_logado(token: Annotated[str, Depends(token_schema)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sem permissão",
        headers={'WWW-Authenticate': 'Bearer'}
    ) # var so para o lancamento da exception

    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITMO])
        email = payload.get('sub')
        if not email:
            raise credentials_exception
        
        usuario = session.scalar(
            select(Usuarios).where(
                Usuarios.email == email
            )
        )
        if not usuario:
            raise credentials_exception
        
        return usuario

    except Exception:
        raise credentials_exception


@login_router.post("/login", response_model=Token)
def login(session: Session = Depends(get_session), form: OAuth2PasswordRequestForm = Depends()):
    usuario = session.scalar(
        select(Usuarios).where(
            Usuarios.email == form.username
        )
    )

    if not usuario:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Erro")
    if not password_hash.verify(form.password, usuario.senha_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Erro")
    
    access_token = create_access_token(
        data={
        'sub': usuario.email
        }
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }