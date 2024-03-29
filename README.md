# FastAPI Logging com  Correlation-ID


## Requerimentos

### poetry
Instalar o poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Configurar integração com o terminal

```bash
# edite o arquivo de configuração do terminal:
sudo nano ~/.zshrc
# ou: sudo nano ~/.bashrc

# adicione a seguinte linha ao arquivo:
export PATH="/home/<your-user>/.local/bin:$PATH"
# o caminho correto será informado ao final do script de instalação do poetry

# recarregue as configurações do terminal:
source ~/.zshrc
# ou: source ~/.bashrc
```

Instalar as dependências do projeto

```bash
poetry install --no-root
```


## Rodando o projeto

```bash
source .venv/bin/activate
uvicorn main:app --reload
```


## Testando o projeto

Em outro terminal, use CURL para acessar a rota /route_one da API.

```bash
curl http://127.0.0.1:8000/route_one
```

Os logs da API deverão aparecer no primeiro terminal demonstrando os Correlation IDs mantidos entre as chamadas:
```bash
INFO      [00000000-0000-0000-0000-000000000000] [Sample FastAPI App] 2024-03-08 14:14:07,785 - Application startup complete.
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,388 - Logging from route_one()
DEBUG     [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,389 - Request called with headers: {'X-Custom': '123', 'X-Correlation-Id': '67725191-13b7-4d9a-bf66-b609c081bd24'}
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,392 - Logging from route_two()
DEBUG     [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,392 - Request called with headers: {'X-Custom': '123', 'X-Correlation-Id': '67725191-13b7-4d9a-bf66-b609c081bd24'}
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,395 - Logging from route_three()
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,397 - 127.0.0.1:34190 - "GET /route_three HTTP/1.1" 200 OK
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,399 - 127.0.0.1:34188 - "GET /route_two HTTP/1.1" 200 OK
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,401 - 127.0.0.1:34184 - "GET /route_one HTTP/1.1" 200 OK
```

Caso seja enviado um Correlation ID pelo header da requisição inicial, este é mantido nas chamadas subsequentes:
```bash
curl -H "X-Correlation-Id: c8f6a9f9-3883-42fc-be6e-5fbe365498c9" http://127.0.0.1:8000/route_one
```

TODO: Demonstrar o comportamento dos Correlation IDs em comunicações entre diferentes serviços
