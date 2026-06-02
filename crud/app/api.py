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
from .routers.auth import login


app = FastAPI()

# Routers
app.include_router(avaliacoes.avaliacoes_router)
app.include_router(categorias.categorias_router)
app.include_router(enderecos.enderecos_router)
app.include_router(estoque.estoque_router)
app.include_router(pagamentos.pagamentos_router)
app.include_router(papeis.papeis_router)
app.include_router(pedidos.pedidos_router)
app.include_router(produtos.produto_router)
app.include_router(users.user_router)
app.include_router(login.login_router)


@app.get("/")
def test():
    return {'mensagem': 'teste'}