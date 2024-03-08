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
export PATH="/home/rafael/.local/bin:$PATH"

# recarregue as configurações do termina:
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

