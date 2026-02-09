# Contribuindo para Perplexity Agent CLI

## 👋 Bem-vindo!

Obrigado por considerar contribuir! Este documento fornece diretrizes para contribuir com o projeto.

---

## 🛠️ Setup de Desenvolvimento

### 1. Fork e Clone

```bash
git clone https://github.com/SEU-USERNAME/perplexity-agent-cli.git
cd perplexity-agent-cli
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências

```bash
pip install -e ".[dev]"
```

---

## 📝 Padrões de Código

### Estilo Python

- Seguir [PEP 8](https://peps.python.org/pep-0008/)
- Máximo 100 caracteres por linha
- Usar type hints sempre que possível
- Docstrings em português, código em inglês

### Type Hints

```python
from typing import Optional, List, Dict

def process_data(items: List[str], config: Optional[Dict] = None) -> bool:
    """Processa dados com configuração opcional."""
    ...
```

### Docstrings

```python
def create_state(goal: str, mode: str) -> RunState:
    """Cria novo estado de execução.
    
    Args:
        goal: Objetivo da sessão
        mode: Modo do agente (ARCHITECT, IMPLEMENTER, etc.)
        
    Returns:
        Estado inicializado
        
    Raises:
        ValueError: Se modo inválido
    """
    ...
```

---

## ✅ Checklist de Commit

Antes de commitar:

```bash
# 1. Linting
flake8 perplexity_cli/

# 2. Type checking
mypy perplexity_cli/

# 3. Testes
pytest

# 4. Cobertura
pytest --cov=perplexity_cli --cov-report=term-missing
```

---

## 🐛 Reportando Bugs

### Template de Issue

```markdown
## Descrição
Descrição clara do bug

## Passos para Reproduzir
1. Execute `perplexity-cli`
2. Digite "..."
3. Observe o erro

## Comportamento Esperado
O que deveria acontecer

## Comportamento Atual
O que acontece

## Ambiente
- OS: Windows 11
- Python: 3.11
- Versão CLI: 0.1.0

## Logs
```
[cole logs aqui]
```
```

---

## ✨ Propondo Features

### Template de Feature Request

```markdown
## Problema
Qual problema isso resolve?

## Solução Proposta
Como você imagina a solução?

## Alternativas
Outras abordagens consideradas

## Exemplo de Uso
```python
# Como seria usado
perplexity-cli --new-feature
```
```

---

## 🔀 Workflow de PR

### 1. Criar Branch

```bash
git checkout -b feature/minha-feature
# ou
git checkout -b fix/corrigir-bug
```

### Convenção de Nomes

- `feature/` - Nova funcionalidade
- `fix/` - Correção de bug
- `docs/` - Apenas documentação
- `test/` - Apenas testes
- `refactor/` - Refatoração sem mudar funcionalidade

### 2. Fazer Mudanças

```bash
# Trabalhe nas mudanças
vim perplexity_cli/cli.py

# Adicione testes
vim tests/test_cli.py

# Execute testes
pytest
```

### 3. Commit

```bash
git add .
git commit -m "feat: adicionar comando /export"
```

#### Convenção de Commits (Conventional Commits)

- `feat:` - Nova feature
- `fix:` - Correção de bug
- `docs:` - Documentação
- `test:` - Testes
- `refactor:` - Refatoração
- `style:` - Formatação, sem mudar lógica
- `chore:` - Tarefas de manutenção

### 4. Push e PR

```bash
git push origin feature/minha-feature
```

Abra PR no GitHub com descrição detalhada.

---

## 🧹 Checklist de PR

Seu PR deve:

- [ ] Passar em todos os testes: `pytest`
- [ ] Ter cobertura ≥ 80%
- [ ] Seguir PEP 8: `flake8`
- [ ] Ter type hints: `mypy`
- [ ] Incluir testes para código novo
- [ ] Atualizar documentação se necessário
- [ ] Ter descrição clara do que muda
- [ ] Referenciar issue relacionada (se houver)

---

## 🎯 Áreas para Contribuir

### Prioridade Alta

- [ ] Implementar execução real de comandos (executor.py)
- [ ] Adicionar integração com Perplexity API
- [ ] Melhorar detecção NLP de intenções
- [ ] Implementar file watcher funcional

### Melhorias

- [ ] Adicionar mais testes de integração
- [ ] Melhorar mensagens de erro
- [ ] Adicionar exemplos de uso
- [ ] Criar tutoriais em vídeo

### Documentação

- [ ] Traduzir docs para inglês
- [ ] Adicionar mais exemplos
- [ ] Criar guia de arquitetura
- [ ] Documentar casos de uso

---

## ❓ Dúvidas?

- Abra uma [Issue](https://github.com/VictorMoraesSantos/perplexity-agent-cli/issues)
- Entre em contato: [seu-email]

---

## 🚀 Obrigado!

Suas contribuições fazem este projeto melhor para todos! 🎉
