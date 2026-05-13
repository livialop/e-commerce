from pydantic import BaseModel, EmailStr
from sqlmodel import Field
from typing import Optional
from decimal import Decimal

# ------------ USUARIO ------------

class UsuarioCreate(BaseModel):
    nome: str = Field(max_length=100)
    email: EmailStr = Field(max_length=120)
    senha: str = Field(max_length=255)

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = Field(default=None, max_length=120)
    senha: Optional[str] = Field(default=None, max_length=255)

class UsuarioPapeisUpdate(BaseModel):
    usuario_id: int
    papel_id: int


# ------------ PRODUTO ------------

class ProdutoCreate(BaseModel):
    nome: str = Field(max_length=150)
    descricao: Optional[str] 
    preco: Decimal = Field(max_digits=10, decimal_places=2)

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=150)
    descricao: Optional[str] = Field(default=None)
    preco: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)

class ProdutoCategoriaUpdate(BaseModel):
    produto_id: int
    categoria_id: int

# ------------ PEDIDO ------------

class PedidoCreate(BaseModel):
    usuario_id: int
    status: Optional[str] = Field(max_length=50)

class PedidoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    total: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    status: Optional[str] = Field(default=None, max_length=50)

# ------------ ITENS PEDIDO ------------
class ItemPedidoCreate(BaseModel):
    produto_id: int
    pedido_id: int
    quantidade: int

# ------------ PAPEIS ------------

class PapelCreate(BaseModel):
    nome: str = Field(max_length=50)

class PapelUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=50)

# ------------ PAGAMENTOS ------------

class PagamentoCreate(BaseModel):
    pedido_id: Optional[int]
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)

class PagamentoUpdate(BaseModel):
    pedido_id: Optional[int] = None
    valor: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    metodo: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=50)

# ------------ ESTOQUE ------------

class EstoqueCreate(BaseModel):
    produto_id: Optional[int]
    quantidade: int

class EstoqueUpdate(BaseModel):
    produto_id: Optional[int] = None
    quantidade: Optional[int] = None

# ------------ ENDERECOS ------------

class EnderecoCreate(BaseModel):
    usuario_id: Optional[int]
    rua: Optional[str] = Field(max_length=150)
    cidade: Optional[str] = Field(max_length=100)
    estado: Optional[str] = Field(max_length=100)
    cep: Optional[str] = Field(max_length=20)

class EnderecoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    rua: Optional[str] = Field(default=None, max_length=150)
    cidade: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, max_length=100)
    cep: Optional[str] = Field(default=None, max_length=20)

# ------------ CATEGORIAS ------------

class CategoriaCreate(BaseModel):
    nome: str = Field(max_length=100)

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, max_length=100)

# ------------ AVALIAÇÕES ------------

class AvaliacaoCreate(BaseModel):
    usuario_id: int
    produto_id: int
    nota: int
    comentario: Optional[str]

class AvaliacaoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    produto_id: Optional[int] = None
    nota: Optional[int] = None
    comentario: Optional[str] = None