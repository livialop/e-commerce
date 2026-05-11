from fastapi import FastAPI
from .routers.avaliacoes import avaliacoes
from .routers.categorias import categorias
from .routers.enderecos import enderecos
from .routers.estoque import estoque
from .routers.pagamentos import pagamentos
from .routers.papeis import papeis
from .routers.pedidos import pedidos
from .routers.produtos import produtos   
from .routers.users import users


app = FastAPI()

# Routers
app.include_router(avaliacoes.router)
app.include_router(categorias.router)
app.include_router(enderecos.router)
app.include_router(estoque.router)
app.include_router(pagamentos.router)
app.include_router(papeis.router)
app.include_router(pedidos.router)
app.include_router(produtos.router)
app.include_router(users.router)


@app.get("/")
def test():
    return {'mensagem': 'teste'}