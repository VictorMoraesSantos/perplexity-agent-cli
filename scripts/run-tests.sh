#!/bin/bash
# Executa testes completos

set -e

echo "=== Executando Testes ==="

# Unit tests com coverage
echo "\n[1/3] Unit tests..."
pytest tests/ -v --cov=perplexity_cli --cov-report=term --cov-report=html

# Linting
echo "\n[2/3] Linting..."
flake8 perplexity_cli --max-line-length=120 --ignore=E203,W503 || true

# Type checking
echo "\n[3/3] Type checking..."
mypy perplexity_cli --ignore-missing-imports || true

echo "\n✓ Testes concluídos!"
echo "Relatório HTML: htmlcov/index.html"
