#!/bin/bash

# Ativa o ambiente virtual (ajuste o caminho se necessário)
if [ -d "./.venv" ]; then
  echo "Ativando ambiente virtual..."
  source ./.venv/bin/activate
else
  echo "Ambiente virtual não encontrado. Instalando dependências..."
  python -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# Inicia a aplicação FastAPI com Gunicorn e UvicornWorker
echo "Iniciando o servidor..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
