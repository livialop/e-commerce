from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import datetime
from decimal import Decimal


def utc() -> datetime.datetime:
    '''Retorna a data atual'''
    return datetime.datetime.now(datetime.timezone.utc)


# Tabelas de conexão

class UsuarioPapeis(SQLModel, table=True):
    __tablename__ = "usuario_papeis"

    usuario_id: int | None = Field(
        default=None, 
        foreign_key="usuarios.id", 
        primary_key=True
    )
    papel_id: int | None = Field(
        default=None, 
        foreign_key="papeis.id", 
        primary_key=True
    )


class ProdutoCategorias(SQLModel, table=True):
    __tablename__ = "produto_categorias"

    produto_id: int | None = Field(
        default=None,
        foreign_key="produtos.id",
        primary_key=True
    )
    categoria_id: int | None = Field(
        default=None,
        foreign_key="categorias.id",
        primary_key=True
    )



# Tabelas 

class Usuarios(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=120, index=True)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime.datetime = Field(default_factory=utc)

    papeis: List["Papeis"] = Relationship(
        back_populates="usuarios",
        link_model=UsuarioPapeis
    )
    pedidos: List["Pedidos"] = Relationship(back_populates="usuario") # o nome do backpopulates tem que ser igual ao nome da variavel que foi declarada na outra classe. aqui é usuario no sing. pq é como eu declarei na tab. de pedidos
    enderecos: List["Enderecos"] = Relationship(back_populates="usuario")
    avaliacoes: List["Avaliacoes"] = Relationship(back_populates="usuario")


class Papeis(SQLModel, table=True):
    __tablename__ = "papeis"
    
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(unique=True, max_length=50)

    usuarios: List["Usuarios"] = Relationship(
        back_populates="papeis",
        link_model=UsuarioPapeis
    )


class Produtos(SQLModel, table=True):
    __tablename__ = "produtos"
    
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150)
    descricao: str | None = Field(default=None)
    preco: Decimal = Field(max_digits=10, decimal_places=2) # mesma coisa que DECIMAL(10,2)
    criado_em: datetime.datetime = Field(default_factory=utc)
    categorias: List["Categorias"] = Relationship(
        back_populates="produtos",
        link_model=ProdutoCategorias
    )
    itens_pedido: List["ItensPedido"] = Relationship(back_populates="produto")
    avaliacoes: List["Avaliacoes"] = Relationship(back_populates="produto")
    estoque: Optional["Estoque"] = Relationship(back_populates="produto")


class Categorias(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)

    produtos: List["Produtos"] = Relationship(
        back_populates="categorias",
        link_model=ProdutoCategorias
    )


class Pedidos(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int | None = Field(
        default=None,
        foreign_key="usuarios.id"
    )
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=50)
    criado_em: datetime.datetime = Field(default_factory=utc)

    usuario: Optional["Usuarios"] = Relationship(back_populates="pedidos")
    itens: List["ItensPedido"] = Relationship(back_populates="pedido")
    pagamentos: List["Pagamentos"] = Relationship(back_populates="pedido")


class ItensPedido(SQLModel, table=True):
    __tablename__ = "itens_pedido"

    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int | None = Field(
        default=None,
        foreign_key="pedidos.id"
    )
    produto_id: int | None = Field(
        default=None,
        foreign_key="produtos.id"
    )
    quantidade: int = Field()
    preco: Decimal = Field(max_digits=10, decimal_places=2)
    pedido: Optional["Pedidos"] = Relationship(back_populates="itens")
    produto: Optional["Produtos"] = Relationship(back_populates="itens_pedido")


class Pagamentos(SQLModel, table=True):
    __tablename__ = "pagamentos"

    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int | None = Field(
        default=None, 
        foreign_key="pedidos.id"
    )
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: datetime.datetime = Field(default_factory=utc)

    pedido: Optional["Pedidos"] = Relationship(back_populates="pagamentos")


class Enderecos(SQLModel, table=True):
    __tablename__ = "enderecos"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int | None = Field(
        default=None, 
        foreign_key="usuarios.id"
    )
    rua: str | None = Field(max_length=150)
    cidade: str | None = Field(max_length=100)
    estado: str | None = Field(max_length=100)
    cep: str | None = Field(max_length=20)

    usuario: Optional["Usuarios"] = Relationship(back_populates="enderecos")


class Avaliacoes(SQLModel, table=True):
    __tablename__ = "avaliacoes"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int | None = Field(
        default=None, 
        foreign_key="usuarios.id"
    )
    produto_id: int | None = Field(
        default=None,
        foreign_key="produtos.id"
    )
    nota: int = Field()
    comentario: str | None = Field(default=None)
    criado_em: datetime.datetime = Field(default_factory=utc)

    usuario: Optional["Usuarios"] = Relationship(back_populates="avaliacoes")
    produto: Optional["Produtos"] = Relationship(back_populates="avaliacoes")


class Estoque(SQLModel, table=True):
    __tablename__ = "estoque"

    id: int | None = Field(default=None, primary_key=True)
    produto_id: int | None = Field(
        default=None, 
        foreign_key="produtos.id",
        unique=True
    )
    quantidade: int = Field()
    atualizado_em: datetime.datetime = Field(default_factory=utc)

    produto: Optional["Produtos"] = Relationship(back_populates="estoque")
