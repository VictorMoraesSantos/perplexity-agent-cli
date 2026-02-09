# Guia de Testes - Perplexity Agent CLI

## 📁 Índice

1. [Instalação](#instalacao)
2. [Execução Rápida](#execucao-rapida)
3. [Tipos de Teste](#tipos-de-teste)
4. [Cobertura](#cobertura)
5. [CI/CD](#cicd)
6. [Troubleshooting](#troubleshooting)

---

## Instalação {#instalacao}

### Instalar Dependências de Teste

```bash
# Com pip
pip install -r requirements-test.txt

# Ou com ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate.bat  # Windows

pip install -r requirements-test.txt
pip install -e .  # Instalar pacote em modo editável
```

---

## Execução Rápida {#execucao-rapida}

### Todos os Testes

```bash
# Linux/Mac
bash scripts/test-complete.sh

# Windows
scripts\test-complete.bat

# Ou diretamente com pytest
pytest tests/ -v
```

### Testes Específicos

```bash
# Apenas testes de estado
pytest tests/test_state_complete.py -v

# Apenas testes de NLP
pytest tests/test_nlp_complete.py -v

# Apenas testes de CLI
pytest tests/test_cli_complete.py -v

# Apenas testes de edge cases
pytest tests/test_edge_cases.py -v
```

### Testes por Categoria

```bash
# Apenas testes críticos
pytest tests/ -m critical

# Apenas testes de segurança
pytest tests/test_edge_cases.py::TestSecurityEdgeCases -v

# Apenas testes lentos
pytest tests/ -m slow
```

---

## Tipos de Teste {#tipos-de-teste}

### 1. Testes Unitários

**O quê:** Testam funções individuais isoladamente

**Como executar:**
```bash
pytest tests/test_state_complete.py tests/test_nlp_complete.py -v
```

**Cobertura esperada:** 90%+

---

### 2. Testes de Integração

**O quê:** Testam interação entre módulos

**Como executar:**
```bash
pytest tests/test_cli_complete.py::TestCLIIntegration -v
```

---

### 3. Testes de Edge Cases

**O quê:** Casos extremos e situações inesperadas

**Como executar:**
```bash
pytest tests/test_edge_cases.py -v
```

**Importante:** Incluem testes de segurança

---

### 4. Testes de Segurança

**O quê:** Tentativas de exploração e ataques

**Como executar:**
```bash
pytest tests/test_edge_cases.py::TestSecurityEdgeCases -v
```

**Exemplos testados:**
- Path traversal
- SQL injection
- XSS
- Comandos maliciosos

---

## Cobertura {#cobertura}

### Gerar Relatório de Cobertura

```bash
# Terminal
pytest tests/ --cov=perplexity_cli --cov-report=term

# HTML (mais detalhado)
pytest tests/ --cov=perplexity_cli --cov-report=html

# Abrir relatório HTML
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov\index.html
```

### Meta de Cobertura

- **Mínimo:** 80%
- **Ideal:** 90%+
- **Crítico:** 100% em `state.py` e `nlp.py`

### Verificar Cobertura Mínima

```bash
pytest tests/ --cov=perplexity_cli --cov-fail-under=80
```

---

## Qualidade de Código

### Linting

```bash
# Flake8
flake8 perplexity_cli --max-line-length=120 --ignore=E203,W503

# Black (formatação)
black perplexity_cli --check

# isort (imports)
isort perplexity_cli --check-only
```

### Type Checking

```bash
mypy perplexity_cli --ignore-missing-imports
```

### Segurança

```bash
# Verifica vulnerabilidades no código
bandit -r perplexity_cli

# Verifica dependências inseguras
safety check
```

---

## Testes Contínuos (Watch Mode)

### Com pytest-watch

```bash
# Instalar
pip install pytest-watch

# Executar
ptw tests/ -- -v
```

Agora os testes executam automaticamente quando você salva um arquivo!

---

## Testes Paralelos

### Acelerar Execução

```bash
# Usar todos os cores
pytest tests/ -n auto

# Usar número específico de cores
pytest tests/ -n 4
```

**Nota:** Requer `pytest-xdist`

---

## CI/CD {#cicd}

### GitHub Actions

Os testes executam automaticamente em:
- Todo push para `main`
- Todo Pull Request
- Múltiplas plataformas: Ubuntu, Windows, macOS
- Múltiplas versões Python: 3.8, 3.9, 3.10, 3.11, 3.12

### Verificar Status no PR

1. Abra seu Pull Request
2. Role até "Checks"
3. Veja resultados dos testes

---

## Troubleshooting {#troubleshooting}

### Problema: Testes falham localmente mas passam no CI

**Solução:**
```bash
# Limpar cache
pytest --cache-clear tests/

# Reinstalar dependências
pip install -r requirements-test.txt --force-reinstall
```

---

### Problema: Import errors

**Solução:**
```bash
# Instalar pacote em modo editável
pip install -e .

# Ou adicionar ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

### Problema: Permissões no Linux/Mac

**Solução:**
```bash
chmod +x scripts/test-complete.sh
bash scripts/test-complete.sh
```

---

### Problema: Testes lentos

**Solução:**
```bash
# Pular testes lentos
pytest tests/ -m "not slow"

# Usar paralelização
pytest tests/ -n auto

# Executar apenas testes modificados
pytest tests/ --lf  # last failed
pytest tests/ --ff  # failed first
```

---

## Boas Práticas

### Antes de Commitar

```bash
# 1. Executar todos os testes
pytest tests/ -v

# 2. Verificar cobertura
pytest tests/ --cov=perplexity_cli --cov-report=term

# 3. Linting
flake8 perplexity_cli

# 4. Formatação
black perplexity_cli
isort perplexity_cli
```

### Ao Adicionar Nova Feature

1. ✅ Escrever testes ANTES do código (TDD)
2. ✅ Garantir cobertura ≥ 80%
3. ✅ Incluir edge cases
4. ✅ Testar com entradas inválidas
5. ✅ Documentar casos de teste

### Ao Corrigir Bug

1. ✅ Escrever teste que reproduz o bug
2. ✅ Verificar que teste falha
3. ✅ Corrigir bug
4. ✅ Verificar que teste passa
5. ✅ Adicionar ao suite de regressão

---

## Estrutura dos Testes

```
tests/
├── test_state_complete.py      # Testes do sistema de estado
├── test_nlp_complete.py         # Testes de detecção de intenção
├── test_cli_complete.py         # Testes da interface CLI
├── test_edge_cases.py           # Edge cases e segurança
├── __init__.py
├── conftest.py                  # Fixtures compartilhados
└── integration/                 # Testes de integração (futuro)
```

---

## Métricas de Qualidade

### Objetivos

| Métrica | Mínimo | Ideal |
|---------|---------|-------|
| Cobertura | 80% | 90%+ |
| Testes Passando | 100% | 100% |
| Flake8 | 0 erros | 0 erros |
| Mypy | 0 erros | 0 warnings |
| Bandit | 0 high | 0 issues |

---

## Recursos Adicionais

- **Plano de Testes Completo:** [TEST_PLAN.md](TEST_PLAN.md)
- **Documentação Pytest:** https://docs.pytest.org/
- **Cobertura:** https://coverage.readthedocs.io/
- **Flake8:** https://flake8.pycqa.org/

---

## Suporte

Se encontrar problemas:

1. Verifique este guia
2. Leia [TEST_PLAN.md](TEST_PLAN.md)
3. Abra uma issue no GitHub

**Lembre-se:** Testes são cruciais para qualidade! 💚
