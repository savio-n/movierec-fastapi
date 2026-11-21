
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cria usuário sem privilégios administrativos
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --home-dir /app appuser

# Instala dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação e os dados
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup data/ ./data/

# Copia o script com permissão de execução
COPY --chown=appuser:appgroup --chmod=755 \
    scripts/start.sh ./scripts/start.sh

USER appuser

EXPOSE 8000

CMD ["./scripts/start.sh"]
