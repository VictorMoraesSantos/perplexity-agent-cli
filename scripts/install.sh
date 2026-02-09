#!/bin/bash
# Script de instalação do Perplexity Agent CLI

set -e

echo "=== Instalando Perplexity Agent CLI ==="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Criar venv se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "✓ Ambiente virtual pronto"

# Ativar venv
source venv/bin/activate

echo "✓ Ambiente ativado"

# Instalar dependências
echo "Instalando dependências..."
pip install --upgrade pip
pip install -e .

echo "✓ Instalação concluída!"
echo ""
echo "Para usar o CLI:"
echo "  1. Ative o ambiente: source venv/bin/activate"
echo "  2. Execute: perplexity-cli"
echo ""
echo "Para ver ajuda: perplexity-cli --help"
