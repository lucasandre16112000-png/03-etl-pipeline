#!/bin/bash

# Script para executar testes do Pipeline ETL no Linux/Mac

echo ""
echo "============================================"
echo "Pipeline ETL - Test Runner"
echo "============================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado! Por favor, instale Python 3.9 ou superior."
    exit 1
fi

# Verificar versão do Python
python3 --version

# Verificar se venv existe, se não, criar
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar ambiente virtual!"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo "[INFO] Ativando ambiente virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao ativar ambiente virtual!"
    exit 1
fi

# Instalar dependências
echo "[INFO] Instalando dependências..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar dependências!"
    exit 1
fi

# Executar testes
echo "[INFO] Executando testes com pytest..."
echo ""
pytest -v --tb=short
exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "[SUCESSO] Todos os testes passaram!"
else
    echo "[ERRO] Alguns testes falharam com código: $exit_code"
fi

exit $exit_code
