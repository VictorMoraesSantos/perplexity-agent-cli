# Perplexity Agent CLI

> Sistema de agente de engenharia de software com checkpoints e rastreabilidade total

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🔍 Visão Geral

O **Perplexity Agent CLI** é um sistema avançado de agente de engenharia que opera com segurança e rastreabilidade total. Ele nunca "se perde" graças ao sistema de checkpoints e estado persistente.

### Principais Características

- **✅ 6 Perfis de Agente**: ARCHITECT, IMPLEMENTER, DEBUGGER, REVIEWER, DOCUMENTER, OPS
- **📦 Sistema de Checkpoints**: Retome de onde parou sem perder contexto
- **📝 Estado Persistente**: Todo o progresso é salvo em JSON rastreável
- **🔍 Pipeline Estruturado**: Etapas A-E garantem qualidade e consistência
- **🚫 Protocolo de Erro**: Diagnóstico automático com hipóteses e correções
- **👁️ Watcher de Filesystem**: Detecta mudanças externas em tempo real
- **🧪 Modo Dry-Run**: Simule ações antes de executar

## 🚀 Instalação

### Clonando o repositório

```bash
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli
```

### Instalação local (desenvolvimento)

```bash
pip install -e .
```

### Instalação via pip (quando publicado)

```bash
pip install perplexity-agent-cli
```

## 📚 Uso Rápido

### Iniciar CLI interativo

```bash
perplexity-cli
```

### Iniciar com objetivo definido

```bash
perplexity-cli --goal "Implementar sistema de autenticação" --mode ARCHITECT
```

### Especificar workspace

```bash
perplexity-cli --workspace /caminho/para/projeto
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
| `/undo` | Desfaz últimas alterações | `/undo` |
| `/help` | Exibe ajuda | `/help` |
| `/exit` ou `/quit` | Sai do CLI | `/exit` |

## 🎭 Perfis de Agente

### ARCHITECT
**Foco**: Arquitetura, estrutura, padrões de design

```bash
/agent ARCHITECT
```

- Define estrutura de pastas
- Escolhe padrões e frameworks
- Especifica contratos de API
- Divide responsabilidades

### IMPLEMENTER
**Foco**: Codificação, features, refatoração

```bash
/agent IMPLEMENTER
```

- Implementa funções e classes
- Cria/modifica arquivos
- Adiciona testes
- Corrige bugs simples

### DEBUGGER
**Foco**: Investigação de erros, diagnóstico, correções cirúrgicas

```bash
/agent DEBUGGER
```

- Analisa stacktraces
- Reproduz bugs
- Propõe hipóteses
- Aplica correções mínimas

### REVIEWER
**Foco**: Qualidade, consistência, segurança

```bash
/agent REVIEWER
```

- Revisa diffs
- Verifica padrões
- Identifica edge cases
- Sugere melhorias

### DOCUMENTER
**Foco**: Documentação, exemplos, comentários

```bash
/agent DOCUMENTER
```

- Atualiza README
- Cria exemplos de uso
- Documenta APIs
- Adiciona docstrings

### OPS
**Foco**: CI/CD, Docker, automações, deploy

```bash
/agent OPS
```

- Configura GitHub Actions
- Cria Dockerfiles
- Scripts de build
- Setup de hooks git

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

### Exemplo de Fluxo

```
✗ ERRO DETECTADO
Local: src/main.py:42
Mensagem: ImportError: No module named 'requests'

Executando diagnóstico automático...
  1. Analisando stacktrace...
  2. Verificando dependências...

Hipóteses:

1. [HIGH] Dependência não instalada
   Sugestão: Adicionar 'requests' em requirements.txt e instalar

2. [MEDIUM] Ambiente virtual incorreto
   Sugestão: Verificar se venv está ativo

Aplicando correção baseada na hipótese principal...
```

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
# 1. Iniciar CLI com objetivo
perplexity-cli --goal "Adicionar testes unitários" --mode IMPLEMENTER

# 2. Verificar status
/status

# 3. Ver plano gerado
/plan

# 4. Ativar dry-run para simular
/dry-run on

# 5. Executar (simulado)
# ... ações do agente ...

# 6. Revisar mudanças propostas
/status

# 7. Aplicar mudanças reais
/dry-run off
/apply

# 8. Trocar para modo REVIEWER
/agent REVIEWER

# 9. Revisar código
# ... ações de review ...

# 10. Sair
/exit
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

## 🛣️ Roadmap

- [ ] Processamento de linguagem natural (LLM integration)
- [ ] Sistema de patches avançado
- [ ] Undo/redo completo com git
- [ ] Interface web (opcional)
- [ ] Plugins e extensões
- [ ] Suporte a múltiplos workspaces simultâneos
- [ ] Telemetria e analytics

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'feat: nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📜 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## ✨ Autor

**Victor Moraes**
- GitHub: [@VictorMoraesSantos](https://github.com/VictorMoraesSantos)
- Website: [victor-moraes.vercel.app](https://victor-moraes.vercel.app/)

---

**Desenvolvido para Perplexity** 🔮
