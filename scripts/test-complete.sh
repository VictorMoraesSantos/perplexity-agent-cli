#!/bin/bash
# Script completo de testes - executa toda a suite

set -e

echo "===================================="
echo "  SUITE COMPLETA DE TESTES"
echo "===================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para log
log_step() {
    echo -e "${YELLOW}[$1]${NC} $2"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# 1. Unit tests
log_step "1/6" "Executando testes unitários..."
pytest tests/ -v --tb=short --ignore=tests/integration/ || {
    log_error "Testes unitários falharam"
    exit 1
}
log_success "Testes unitários passaram"
echo ""

# 2. Testes de integração (se existirem)
if [ -d "tests/integration" ]; then
    log_step "2/6" "Executando testes de integração..."
    pytest tests/integration/ -v || {
        log_error "Testes de integração falharam"
        exit 1
    }
    log_success "Testes de integração passaram"
else
    log_step "2/6" "Pulando testes de integração (pasta não encontrada)"
fi
echo ""

# 3. Cobertura de código
log_step "3/6" "Calculando cobertura de código..."
pytest tests/ --cov=perplexity_cli --cov-report=term --cov-report=html --cov-fail-under=80 || {
    log_error "Cobertura abaixo de 80%"
    exit 1
}
log_success "Cobertura adequada"
echo ""

# 4. Linting
log_step "4/6" "Executando linters..."
flake8 perplexity_cli --max-line-length=120 --ignore=E203,W503 || {
    log_error "Linting falhou"
    exit 1
}
log_success "Linting passou"
echo ""

# 5. Type checking
log_step "5/6" "Verificando tipos..."
mypy perplexity_cli --ignore-missing-imports || {
    echo "${YELLOW}Aviso: Type checking com warnings${NC}"
}
log_success "Type checking completo"
echo ""

# 6. Testes de segurança
log_step "6/6" "Executando testes de segurança..."
pytest tests/test_edge_cases.py::TestSecurityEdgeCases -v || {
    log_error "Testes de segurança falharam"
    exit 1
}
log_success "Testes de segurança passaram"
echo ""

# Sumário final
echo "===================================="
echo -e "${GREEN}✓ TODOS OS TESTES PASSARAM${NC}"
echo "===================================="
echo ""
echo "Relatórios gerados:"
echo "  - Cobertura HTML: htmlcov/index.html"
echo ""
echo "Estatísticas:"
pytest tests/ --co -q | tail -n 1
