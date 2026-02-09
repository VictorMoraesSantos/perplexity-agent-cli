# Perplexity Agent CLI

> Sistema de agente de engenharia de software com checkpoints e rastreabilidade total

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/VictorMoraesSantos/perplexity-agent-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/VictorMoraesSantos/perplexity-agent-cli/actions/workflows/tests.yml)
[![Lint](https://github.com/VictorMoraesSantos/perplexity-agent-cli/actions/workflows/lint.yml/badge.svg)](https://github.com/VictorMoraesSantos/perplexity-agent-cli/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/VictorMoraesSantos/perplexity-agent-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/VictorMoraesSantos/perplexity-agent-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🔍 Visão Geral

O **Perplexity Agent CLI** é um sistema avançado de agente de engenharia que opera com segurança e rastreabilidade total. Ele nunca "se perde" graças ao sistema de checkpoints e estado persistente.

### Principais Características

- **✅ 6 Perfis de Agente**: ARCHITECT, IMPLEMENTER, DEBUGGER, REVIEWER, DOCUMENTER, OPS
- **🤖 Modo AUTO**: Detecção automática de intenção via NLP
- **💬 Linguagem Natural**: Digite comandos naturalmente, sem sintaxe complexa
- **📦 Sistema de Checkpoints**: Retome de onde parou sem perder contexto
- **📝 Estado Persistente**: Todo o progresso é salvo em JSON rastreavel
- **🔍 Pipeline Estruturado**: Etapas A-E garantem qualidade e consistência
- **🚫 Protocolo de Erro**: Diagnóstico automático com hipóteses e correções
- **👁️ Watcher de Filesystem**: Detecta mudanças externas em tempo real
- **🧪 Modo Dry-Run**: Simule ações antes de executar
- **✅ Cobertura de Testes 80%+**: Suite completa de testes com CI/CD

## 🚀 Instalação

### Clonando o repositório

```bash
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli
```

### Instalação local (desenvolvimento)

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Veja [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) para guia completo no Windows.

### Instalação via pip (quando publicado)

```bash
pip install perplexity-agent-cli
```

## 📚 Uso Rápido

### 🌟 Modo AUTO (Recomendado)

Digite comandos naturalmente - o agente detecta automaticamente o modo:

```bash
perplexity-cli

[AUTO] > criar uma API REST em Python
→ Modo detectado: IMPLEMENTER
→ Objetivo: Criar uma API REST em Python
✓ Pronto para executar!

[AUTO] > adicionar testes unitários
→ Modo detectado: IMPLEMENTER
→ Objetivo: Adicionar testes unitários

[AUTO] > corrigir bug no arquivo auth.py
→ Modo detectado: DEBUGGER
→ Objetivo: Corrigir bug no arquivo auth.py

[AUTO] > revisar o código
→ Modo detectado: REVIEWER
→ Objetivo: Revisar o código

[AUTO] > documentar a API
→ Modo detectado: DOCUMENTER
→ Objetivo: Documentar a API
```

### Modo Legado (com flags)

```bash
# Com objetivo definido
perplexity-cli --goal "Implementar sistema de autenticação" --mode ARCHITECT

# Com workspace específico
perplexity-cli --workspace /caminho/para/projeto

# Forçar modo manual (sem AUTO)
perplexity-cli --no-auto
```

## 🛠️ Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|----------|
| `/agent <modo>` | Troca o modo do agente | `/agent IMPLEMENTER` |
| `/workspace <path>` | Muda ou exibe workspace | `/workspace /tmp/projeto` |
| `/status` | Mostra estado completo | `/status` |
| `/plan` | Exibe plano e checkpoints | `/plan` |
| `/resume` | Retoma do último checkpoint | `/resume` |
| `/dry-run on\|off` | Ativa/desativa modo simulação | `/dry-run on` |
| `/apply` | Aplica patches pendentes | `/apply` |
| `/watch on\|off` | Liga/desliga watcher | `/watch on` |
| `/auto on\|off` | Liga/desliga detecção AUTO | `/auto off` |
| `/undo` | Desfaz últimas alterações | `/undo` |
| `/help` | Exibe ajuda | `/help` |
| `/exit` ou `/quit` | Sai do CLI | `/exit` |

## 🎭 Perfis de Agente

### ARCHITECT
**Foco**: Arquitetura, estrutura, padrões de design

**Palavras-chave**: arquitetura, estrutura, estruturar, organizar, planejar, design, padrão

```bash
/agent ARCHITECT
```

- Define estrutura de pastas
- Escolhe padrões e frameworks
- Especifica contratos de API
- Divide responsabilidades

### IMPLEMENTER
**Foco**: Codificação, features, refatoração

**Palavras-chave**: implementar, criar, adicionar, desenvolver, codificar, escrever

```bash
/agent IMPLEMENTER
```

- Implementa funções e classes
- Cria/modifica arquivos
- Adiciona testes
- Corrige bugs simples

### DEBUGGER
**Foco**: Investigação de erros, diagnóstico, correções cirúrgicas

**Palavras-chave**: corrigir, bug, erro, problema, falha, debugar, investigar

```bash
/agent DEBUGGER
```

- Analisa stacktraces
- Reproduz bugs
- Propõe hipóteses
- Aplica correções mínimas

### REVIEWER
**Foco**: Qualidade, consistência, segurança

**Palavras-chave**: revisar, review, verificar, checar, validar, analisar código

```bash
/agent REVIEWER
```

- Revisa diffs
- Verifica padrões
- Identifica edge cases
- Sugere melhorias

### DOCUMENTER
**Foco**: Documentação, exemplos, comentários

**Palavras-chave**: documentar, documentação, readme, docs, explicar

```bash
/agent DOCUMENTER
```

- Atualiza README
- Cria exemplos de uso
- Documenta APIs
- Adiciona docstrings

### OPS
**Foco**: CI/CD, Docker, automações, deploy

**Palavras-chave**: deploy, ci, cd, docker, container, pipeline, build

```bash
/agent OPS
```

- Configura GitHub Actions
- Cria Dockerfiles
- Scripts de build
- Setup de hooks git

## 🧪 Testes

### Executar testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=perplexity_cli --cov-report=html

# Testes específicos
pytest tests/test_cli.py

# Pular testes lentos
pytest -m "not slow"
```

### Estrutura de testes

```
tests/
├── test_cli.py              # Testes do CLI
├── test_cli_complete.py     # Testes completos
├── test_commands.py         # Testes dos comandos
├── test_state_complete.py   # Testes de estado
├── test_nlp_complete.py     # Testes NLP
├── test_executor.py         # Testes do executor
├── test_error_protocol.py   # Testes de erros
├── test_filesystem.py       # Testes de filesystem
├── test_watcher.py          # Testes do watcher
├── test_edge_cases.py       # Casos extremos
└── test_integration.py      # Testes E2E
```

Veja [TESTING.md](TESTING.md) para guia completo.

### CI/CD

O projeto usa GitHub Actions para:
- ✅ Testes em Python 3.9, 3.10, 3.11, 3.12
- ✅ Testes em Ubuntu, Windows, macOS
- ✅ Linting com flake8, black, isort
- ✅ Type checking com mypy
- ✅ Cobertura com codecov

## 📊 Pipeline de Execução (Etapas A-E)

Toda tarefa não-trivial segue este fluxo:

### Etapa A — Entendimento e Critérios
- Reescreve objetivo em 1-2 linhas
- Define Definition of Done (DoD)
- Alinha com perfil do agente ativo

### Etapa B — Inventário do Repo
- Lista estrutura de pastas
- Executa `git status`
- Faz `grep` por termos relevantes

### Etapa C — Plano com Checkpoints
- Cria plano enumerado
- Insere checkpoints formais
- Formato: `Checkpoint: CPX:nome`

### Etapa D — Execução Incremental
- Lê arquivos-alvo
- Aplica mudanças localizadas
- Valida com `git diff` e testes
- Atualiza checkpoint ao concluir

### Etapa E — Fechamento
- Lista arquivos alterados
- Mostra próximos passos
- Atualiza RUN_STATE

## 💾 Estado Persistente (RUN_STATE)

O sistema mantém estado serializável em `.perplexity-cli/state.json`:

```json
{
  "workspace": "/caminho/projeto",
  "agent_mode": "IMPLEMENTER",
  "goal": "Adicionar autenticação",
  "current_plan_step": 3,
  "current_checkpoint": "CP2:implementation-done",
  "last_successful_checkpoint": "CP2:implementation-done",
  "open_questions": [],
  "files_touched": ["src/auth.py", "tests/test_auth.py"],
  "commands_run": [
    {"cmd": "pytest", "result": "ok", "ts": "2026-02-09T01:00:00"}
  ],
  "last_error": null,
  "next_action": "Executar testes de integração"
}
```

### Retomada Exata

Se houver erro ou interrupção:

```bash
/resume
```

O sistema:
1. Identifica `last_successful_checkpoint`
2. Recarrega contexto
3. Retoma de `next_action`

## ⚠️ Protocolo de Erro (Obrigatório)

Quando um comando falha:

1. **Captura e registro** em `last_error`
2. **2 ações de diagnóstico** automáticas
3. **Propõe 1 hipótese principal + 1 alternativa**
4. **Aplica correção mínima**
5. **Reexecuta comando**
6. Se falhar novamente: **para e pergunta ao usuário**

## 👁️ Watcher de Filesystem

Monitora mudanças externas em tempo real:

```bash
/watch on
```

Quando detecta alteração:
- Lê arquivo modificado
- Atualiza plano se necessário
- Evita conflitos (merge inteligente)
- Registra evento no RUN_STATE

**Padrões ignorados**: `.git`, `__pycache__`, `.pyc`, `node_modules`, `.venv`

## 🧪 Modo Dry-Run

Simule todas as ações sem modificar arquivos:

```bash
/dry-run on
```

Todas as operações mostram `[DRY-RUN]` e apenas exibem o que fariam.

Para aplicar as mudanças:

```bash
/dry-run off
/apply
```

## 📝 Exemplo Completo

```bash
# 1. Iniciar CLI (modo AUTO)
perplexity-cli

# 2. Dar comando natural
[AUTO] > criar testes unitários para o módulo auth

→ Modo detectado: IMPLEMENTER
→ Objetivo: Criar testes unitários para o módulo auth

# 3. Verificar plano
[AUTO] > /plan

# 4. Ativar dry-run
[AUTO] > /dry-run on

# 5. Continuar trabalhando naturalmente
[AUTO] > adicionar teste para login
[AUTO] > adicionar teste para logout

# 6. Revisar
[AUTO] > /status

# 7. Aplicar
[AUTO] > /dry-run off
[AUTO] > /apply

# 8. Trocar para reviewer
[AUTO] > /agent REVIEWER

# 9. Ou usar linguagem natural
[AUTO] > revisar os testes criados

→ Modo detectado: REVIEWER

# 10. Sair
[AUTO] > /exit
```

## 🔒 Segurança

- **Nunca exfiltra secrets**: Detecta `.env`, tokens, credenciais
- **Modo dry-run**: Teste antes de executar
- **Rastreabilidade total**: Todo comando é registrado
- **Git-aware**: Integra com git para controle de versão

## 🧰 Arquitetura

```
perplexity_cli/
├── __init__.py          # Inicialização
├── cli.py               # Interface principal
├── commands.py          # Handlers de comandos
├── state.py             # Sistema de estado persistente
├── models.py            # Modelos e perfis de agente
├── nlp.py               # Detecção de intenção (NLP)
├── executor.py          # Pipeline A-E
├── error_protocol.py    # Tratamento de erros
├── filesystem.py        # Operações de arquivos
├── watcher.py           # Watcher de filesystem
└── utils.py             # Utilitários
```

## 📦 Dependências

- `click` >= 8.0.0 - Interface de linha de comando
- `rich` >= 13.0.0 - Output rico e colorido
- `watchdog` >= 3.0.0 - Monitoramento de filesystem
- `gitpython` >= 3.1.0 - Integração com Git
- `pytest` >= 7.0.0 - Framework de testes
- `pytest-cov` >= 4.0.0 - Cobertura de código

## 🛣️ Roadmap

- [x] Modo AUTO com detecção NLP
- [x] Suite completa de testes (80%+ cobertura)
- [x] CI/CD com GitHub Actions
- [ ] Processamento de linguagem natural com LLM
- [ ] Sistema de patches avançado
- [ ] Undo/redo completo com git
- [ ] Interface web (opcional)
- [ ] Plugins e extensões
- [ ] Suporte a múltiplos workspaces simultâneos
- [ ] Telemetria e analytics

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes.

### Quick Start

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Adicione testes para sua feature
4. Execute `pytest` e garanta 80%+ cobertura
5. Commit com Conventional Commits (`git commit -am 'feat: nova feature'`)
6. Push para a branch (`git push origin feature/nova-feature`)
7. Abra um Pull Request

## 📜 Documentação Adicional

- [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) - Guia de instalação Windows
- [TESTING.md](TESTING.md) - Guia completo de testes
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guia de contribuição

## 📜 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## ✨ Autor

**Victor Moraes**
- GitHub: [@VictorMoraesSantos](https://github.com/VictorMoraesSantos)
- Website: [victor-moraes.vercel.app](https://victor-moraes.vercel.app/)

---

**Desenvolvido para Perplexity** 🔮
