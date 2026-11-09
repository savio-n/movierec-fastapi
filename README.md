# Sistema de Recomendação com FastAPI e Docker

Este projeto implementa um modelo de recomendação baseado em conteúdo (TF-IDF + Cosine Similarity) empacotado em uma API RESTful com FastAPI e containerizado via Docker.

## Endpoints Principais

- `GET /docs`: Documentação interativa (Swagger UI)
- `POST /items/`: Cadastra novos itens na base
- `POST /users/preferences/`: Atualiza preferências do usuário
- `GET /recommendations/{user_id}`: Retorna os itens recomendados

## Como Executar

### Utilizando Docker Compose (Recomendado)
```bash
docker-compose up --build
```
Acesse a aplicação em `http://localhost:8000/docs`.

### Execução Local (Python)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Rodando os Testes Unitários
```bash
pytest
```
