# Sistema de Recomendação com FastAPI e Docker

Este projeto implementa um modelo de recomendação baseado em conteúdo (TF-IDF + Cosine Similarity) empacotado em uma API RESTful com FastAPI e containerizado via Docker.

## Endpoints Principais

- `GET /docs`: Documentação interativa (Swagger UI)
- `POST /items/`: Cadastra novos itens na base
- `POST /users/preferences/`: Atualiza preferências do usuário
- `GET /recommendations/{user_id}`: Retorna os itens recomendados

## Configuração do Ambiente Virtual

Para executar a aplicação localmente com Python, recomenda-se criar um ambiente virtual para isolar as dependências do projeto. **Esta etapa não é necessária para a execução com Docker.**

Na raiz do repositório, crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente de acordo com seu sistema operacional:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Com o ambiente ativado, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Para desativar o ambiente virtual, execute `deactivate`.


## Como Executar

### Utilizando Docker Compose (Recomendado)

```bash
docker compose up --build -d
```

Acesse a aplicação em `http://localhost:8000/docs`.

Para acompanhar os logs:

```bash
docker compose logs -f api
```

Para encerrar a aplicação:

```bash
docker compose down
```

### Execução Local (Python)

Com o ambiente virtual configurado e as dependências instaladas:

```bash
uvicorn app.main:app --reload
```

Acesse `http://localhost:8000/docs`.

### Rodando os Testes Unitários

Com as dependências instaladas no ambiente virtual:

```bash
python -m pytest
```
