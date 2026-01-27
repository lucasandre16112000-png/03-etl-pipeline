#!/bin/bash

# Script para executar o exemplo do Pipeline ETL no Linux/Mac

echo ""
echo "============================================"
echo "Pipeline ETL - Linux/Mac Launcher"
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

# Executar exemplo
echo "[INFO] Executando pipeline..."
echo ""
python example_usage.py
exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "[SUCESSO] Pipeline executado com sucesso!"
else
    echo "[ERRO] Pipeline falhou com código de erro: $exit_code"
fi

exit $exit_code
