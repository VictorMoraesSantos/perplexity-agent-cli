# Guia de Testes - Perplexity Agent CLI

## 🛠️ Setup

### Instalar dependências de teste

```bash
pip install -e ".[dev]"
```

Ou instalar manualmente:

```bash
pip install pytest pytest-cov pytest-mock coverage
```

---

## 🎯 Executando Testes

### Todos os testes

```bash
pytest
```

### Testes específicos

```bash
# Por arquivo
pytest tests/test_cli.py

# Por classe
pytest tests/test_cli.py::TestCommandAgent

# Por função
pytest tests/test_cli.py::TestCommandAgent::test_change_agent_mode_valid
```

### Com verbosidade

```bash
pytest -v
pytest -vv  # Extra verbose
```

### Pular testes lentos

```bash
pytest -m "not slow"
```

### Apenas testes rápidos

```bash
pytest -m "not integration"
```

---

## 📊 Cobertura de Código

### Gerar relatório de cobertura

```bash
pytest --cov=perplexity_cli --cov-report=html
```

### Ver relatório no terminal

```bash
pytest --cov=perplexity_cli --cov-report=term-missing
```

### Abrir relatório HTML

```bash
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Relatório completo

```bash
coverage run -m pytest
coverage report
coverage html
```

---

## 📝 Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures globais
├── test_cli.py              # Testes básicos do CLI
├── test_cli_complete.py     # Testes completos do CLI
├── test_commands.py         # Testes dos comandos /
├── test_state.py            # Testes básicos de estado
├── test_state_complete.py   # Testes completos de estado
├── test_nlp_complete.py     # Testes do detector NLP
├── test_executor.py         # Testes do executor
├── test_error_protocol.py   # Testes de handling de erros
├── test_filesystem.py       # Testes de operações FS
├── test_watcher.py          # Testes do file watcher
├── test_edge_cases.py       # Testes de casos extremos
└── test_integration.py      # Testes de integração E2E
```

---

## 🧪 Fixtures Disponíveis

### `temp_workspace`
Workspace temporário limpo para testes.

```python
def test_exemplo(temp_workspace):
    # temp_workspace é um Path temporário
    file = Path(temp_workspace) / "test.txt"
    file.write_text("teste")
```

### `state_manager`
StateManager pré-configurado.

```python
def test_exemplo(state_manager):
    state_manager.state.goal = "Novo objetivo"
    state_manager.save()
```

### `console_mock`
Mock do Rich Console.

```python
def test_exemplo(console_mock):
    console_mock.print("teste")
    assert console_mock.print.called
```

---

## ⚙️ Configuração

### `pytest.ini`

Configurado para:
- Cobertura automática com `--cov`
- Relatórios HTML e terminal
- Markers customizados (`slow`, `integration`)
- Output limpo e organizado

### `.coveragerc`

Configurado para:
- Excluir arquivos de teste da cobertura
- Ignorar linhas de debug e abstratas
- Gerar relatórios em `htmlcov/`

---

## 🐞 Debug de Testes

### Com pdb

```bash
pytest --pdb
```

### Parar no primeiro erro

```bash
pytest -x
```

### Mostrar print statements

```bash
pytest -s
```

### Modo verboso com traceback completo

```bash
pytest -vv --tb=long
```

---

## 🏆 Metas de Cobertura

| Módulo | Cobertura Atual | Meta |
|--------|----------------|------|
| `cli.py` | 85% | 90% |
| `state.py` | 95% | 95% |
| `commands.py` | 80% | 85% |
| `nlp.py` | 90% | 95% |
| `models.py` | 100% | 100% |
| `executor.py` | 70% | 80% |
| `filesystem.py` | 75% | 85% |
| `watcher.py` | 65% | 75% |
| **TOTAL** | **80%** | **85%** |

---

## ✅ Checklist de PR

Antes de submeter PR, certifique-se:

- [ ] Todos os testes passam: `pytest`
- [ ] Cobertura ≥ 80%: `pytest --cov`
- [ ] Sem warnings: `pytest --strict-warnings`
- [ ] Linting OK: `flake8 perplexity_cli/`
- [ ] Type hints OK: `mypy perplexity_cli/`
- [ ] Testes novos para código novo
- [ ] Docstrings atualizadas

---

## 📚 Recursos

- [Pytest Docs](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Pytest-cov](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
