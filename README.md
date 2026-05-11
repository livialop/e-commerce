# E-Commerce
Projeto feito como atividade para a matéria de POAS.

## Como executar
1. Clone esse repositório e navegue até ele.
2. Crie o banco de dados no MySQL, crie um arquivo .env (veja as chaves [nesse arquivo](crud/database/database.py)) e se conecte ao banco.
3. Crie as tabelas.
4. Crie o ambiente virtual.
> [!NOTE]
> Se não sabe como, clique [aqui](https://github.com/livialop/Banquinho/blob/main/wikis/ambientesvirtuais.md).
5. Instale as dependências do projeto com `pip install -r requirements.txt`
6. Após isso, basta iniciar o projeto no terminal com:
```bash
python3 main.py
```
Para visualizar e testar os endpoints, basta ir em `127.0.0.1:8000/docs`.