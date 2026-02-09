#!/bin/bash
# Setup de ambiente de desenvolvimento

set -e

echo "=== Setup de Desenvolvimento ==="

# Instalar modo editável
pip install -e .

# Instalar ferramentas de desenvolvimento
echo "Instalando ferramentas de desenvolvimento..."
pip install pytest pytest-cov black flake8 isort mypy

echo "✓ Setup completo!"
echo ""
echo "Comandos disponíveis:"
echo "  pytest                  - Executar testes"
echo "  pytest --cov            - Testes com cobertura"
echo "  black perplexity_cli    - Formatar código"
echo "  flake8 perplexity_cli   - Lint"
echo "  isort perplexity_cli    - Ordenar imports"
