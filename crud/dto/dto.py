from pydantic import BaseModel, EmailStr
from sqlmodel import Field
from typing import Optional
from decimal import Decimal

# ------------ USUARIO ------------

class UsuarioCreate(BaseModel):
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=120)
    senha: str = Field(max_length=255)

# ------------ PRODUTO ------------

class ProdutoCreate(BaseModel):
    nome: str = Field(max_length=150)
    descricao: Optional[str] 
    preco: Decimal = Field(max_digits=10, decimal_places=2)

# ------------ PEDIDO ------------

class PedidoCreate(BaseModel):
    usuario_id: int
    total: Optional[Decimal] = Field(max_digits=10, decimal_places=2)
    status: Optional[str] = Field(max_length=50)

# ------------ PAPEIS ------------

class PapelCreate(BaseModel):
    nome: str = Field(max_length=50)

# ------------ PAGAMENTOS ------------

class PagamentoCreate(BaseModel):
    pedido_id: Optional[int]
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)

# ------------ ESTOQUE ------------

class EstoqueCreate(BaseModel):
    produto_id: Optional[int]
    quantidade: int

# ------------ ENDERECOS ------------

class EnderecoCreate(BaseModel):
    usuario_id: Optional[int]
    rua: Optional[str] = Field(max_length=150)
    cidade: Optional[str] = Field(max_length=100)
    estado: Optional[str] = Field(max_length=100)
    cep: Optional[str] = Field(max_length=20)

# ------------ CATEGORIAS ------------

class CategoriaCreate(BaseModel):
    nome: str = Field(max_length=100)

# ------------ AVALIAÇÕES ------------

class AvaliacaoCreate(BaseModel):
    usuario_id: int
    produto_id: int
    nota: int
    comentario: Optional[str]