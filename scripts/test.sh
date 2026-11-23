
#!/bin/sh
set -eu

# Executa na raiz do projeto
cd "$(dirname "$0")/.."

# Seleciona o interpretador Python
if [ -x .venv/bin/python ]; then
    PYTHON=.venv/bin/python
elif command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

# Verifica as dependências de teste
if ! "$PYTHON" -c "import pytest; import pytest_cov" 2>/dev/null; then
    echo "ERROR: Test dependencies are missing."
    echo "Run: $PYTHON -m pip install -r requirements-dev.txt"
    exit 1
fi

# Define o diretório padrão
if [ "$#" -eq 0 ]; then
    set -- tests/
fi

echo "Running MovieRec tests..."

exec "$PYTHON" -m pytest \
    -v \
    --cov=app \
    --cov-report=term-missing \
    "$@"
