# Plano de Testes Completo - Perplexity Agent CLI

## 🎯 Objetivo

Garantir qualidade total do CLI com cobertura de 100% dos casos de uso, edge cases e cenários de erro.

## 📋 Índice

1. [Escopo de Testes](#escopo)
2. [Tipos de Teste](#tipos)
3. [Casos de Teste](#casos)
4. [Critérios de Aceitação](#criterios)
5. [Ambientes](#ambientes)
6. [Execução](#execucao)

---

## 1. Escopo de Testes {#escopo}

### Módulos a Testar

- ☑️ **cli.py** - Interface principal e loop interativo
- ☑️ **state.py** - Sistema de estado persistente
- ☑️ **models.py** - Perfis de agente e enums
- ☑️ **nlp.py** - Detecção de intenção
- ☑️ **commands.py** - Handlers de comandos
- ☑️ **executor.py** - Pipeline de execução
- ☑️ **error_protocol.py** - Tratamento de erros
- ☑️ **filesystem.py** - Operações de arquivos
- ☑️ **watcher.py** - Monitor de filesystem
- ☑️ **utils.py** - Utilitários

### Funcionalidades Críticas

1. **Sistema de Checkpoints** (🔴 Prioridade Máxima)
2. **Persistência de Estado** (🔴 Prioridade Máxima)
3. **Detecção de Modo** (🟡 Alta)
4. **Comandos /** (🟡 Alta)
5. **Linguagem Natural** (🟡 Alta)
6. **Protocolo de Erro** (🟡 Alta)
7. **Watcher de Arquivos** (🟠 Média)
8. **Modo Dry-Run** (🟠 Média)

---

## 2. Tipos de Teste {#tipos}

### 2.1 Testes Unitários

**Objetivo:** Testar cada função/método isoladamente

**Cobertura Alvo:** 90%+

**Ferramentas:**
- pytest
- pytest-cov
- pytest-mock

### 2.2 Testes de Integração

**Objetivo:** Testar interação entre módulos

**Cenários:**
- CLI → StateManager → JSON
- CLI → NLP → Commands
- ErrorProtocol → StateManager

### 2.3 Testes End-to-End (E2E)

**Objetivo:** Simular uso real do usuário

**Ferramentas:**
- Click Testing (CliRunner)
- Simulação de input

### 2.4 Testes de Edge Cases

**Objetivo:** Cobrir casos extremos e inesperados

**Exemplos:**
- Arquivos corrompidos
- Paths inválidos
- Entrada vazia
- Unicode/emojis
- Comandos malformados

### 2.5 Testes de Performance

**Objetivo:** Garantir performance aceitável

**Métricas:**
- Tempo de inicialização < 1s
- Tempo de comando < 100ms
- Uso de memória < 100MB

### 2.6 Testes de Compatibilidade

**Plataformas:**
- Windows 10/11
- Linux (Ubuntu, Debian)
- macOS (Intel, Apple Silicon)

**Python:**
- 3.8, 3.9, 3.10, 3.11, 3.12

---

## 3. Casos de Teste {#casos}

### 3.1 Sistema de Estado (state.py)

#### TC-STATE-001: Criação de Estado Inicial
**Pré-condições:** Nenhum estado existe
**Passos:**
1. Criar StateManager
2. Chamar create_initial_state("Teste")
3. Verificar estado criado

**Resultado Esperado:**
- Estado criado com goal="Teste"
- Checkpoint = CP0:init
- Arquivo JSON criado

**Prioridade:** 🔴 Crítica

---

#### TC-STATE-002: Persistência de Estado
**Pré-condições:** Estado criado
**Passos:**
1. Criar estado
2. Salvar com save()
3. Criar novo StateManager
4. Carregar com load()

**Resultado Esperado:**
- Estado carregado é idêntico ao salvo
- Todos os campos preservados

**Prioridade:** 🔴 Crítica

---

#### TC-STATE-003: Atualização de Checkpoint
**Passos:**
1. Criar estado
2. update_checkpoint("CP1:test")
3. Verificar current_checkpoint
4. Verificar last_successful_checkpoint

**Resultado Esperado:**
- current_checkpoint = "CP1:test"
- last_successful_checkpoint = "CP1:test"
- Estado salvo automaticamente

**Prioridade:** 🔴 Crítica

---

#### TC-STATE-004: Tratamento de Arquivo Corrompido
**Passos:**
1. Criar arquivo state.json inválido
2. Tentar load()

**Resultado Esperado:**
- Retorna None
- Não lança exceção
- Log de erro exibido

**Prioridade:** 🟡 Alta

---

#### TC-STATE-005: Múltiplos Comandos no Histórico
**Passos:**
1. Adicionar 100 comandos com add_command()
2. Salvar e carregar

**Resultado Esperado:**
- Todos comandos preservados
- Ordem mantida
- Performance aceitável

**Prioridade:** 🟠 Média

---

### 3.2 Detecção de Intenção (nlp.py)

#### TC-NLP-001: Detectar IMPLEMENTER
**Input:** "criar uma API REST"
**Esperado:** AgentMode.IMPLEMENTER
**Prioridade:** 🟡 Alta

---

#### TC-NLP-002: Detectar DEBUGGER
**Input:** "corrigir bug no auth.py"
**Esperado:** AgentMode.DEBUGGER
**Prioridade:** 🟡 Alta

---

#### TC-NLP-003: Detectar REVIEWER
**Input:** "revisar o código"
**Esperado:** AgentMode.REVIEWER
**Prioridade:** 🟡 Alta

---

#### TC-NLP-004: Detectar ARCHITECT
**Input:** "definir estrutura do projeto"
**Esperado:** AgentMode.ARCHITECT
**Prioridade:** 🟡 Alta

---

#### TC-NLP-005: Detectar DOCUMENTER
**Input:** "documentar a API"
**Esperado:** AgentMode.DOCUMENTER
**Prioridade:** 🟡 Alta

---

#### TC-NLP-006: Detectar OPS
**Input:** "configurar CI/CD"
**Esperado:** AgentMode.OPS
**Prioridade:** 🟡 Alta

---

#### TC-NLP-007: Entrada Ambígua
**Input:** "fazer algo"
**Esperado:** AgentMode.IMPLEMENTER (padrão)
**Prioridade:** 🟠 Média

---

#### TC-NLP-008: Extração de Goal
**Input:** "quero criar uma API"
**Esperado:** "Criar uma API"
**Prioridade:** 🟡 Alta

---

#### TC-NLP-009: Unicode e Acentos
**Input:** "criação de módulo de autenticação"
**Esperado:** Detecta corretamente
**Prioridade:** 🟠 Média

---

### 3.3 Interface CLI (cli.py)

#### TC-CLI-001: Inicialização Simples
**Comando:** `perplexity-cli`
**Esperado:**
- CLI inicia sem erros
- Mostra welcome message
- Prompt [AUTO] > exibido

**Prioridade:** 🔴 Crítica

---

#### TC-CLI-002: Inicialização com Goal
**Comando:** `perplexity-cli --goal "Teste" --mode ARCHITECT`
**Esperado:**
- Estado criado automaticamente
- Modo ARCHITECT ativo
- Goal = "Teste"

**Prioridade:** 🟡 Alta

---

#### TC-CLI-003: Workspace Customizado
**Comando:** `perplexity-cli --workspace /tmp/test`
**Esperado:**
- Workspace definido corretamente
- Arquivo state.json em /tmp/test/.perplexity-cli/

**Prioridade:** 🟡 Alta

---

#### TC-CLI-004: Comando Natural Válido
**Input:** "criar uma API"
**Esperado:**
- Modo detectado
- Estado criado/atualizado
- Mensagem de confirmação

**Prioridade:** 🟡 Alta

---

#### TC-CLI-005: Comando Muito Curto
**Input:** "oi"
**Esperado:**
- Mensagem de erro amigável
- Exemplos mostrados
- Não cria estado

**Prioridade:** 🟠 Média

---

#### TC-CLI-006: Saudação
**Input:** "ola"
**Esperado:**
- Responde "Olá!"
- Mostra exemplos
- Não processa como comando

**Prioridade:** 🟠 Média

---

#### TC-CLI-007: Comando / Vazio
**Input:** "/"
**Esperado:**
- Mensagem de erro
- Lista comandos disponíveis

**Prioridade:** 🟠 Média

---

#### TC-CLI-008: Ctrl+C (Interrupção)
**Ação:** Pressionar Ctrl+C
**Esperado:**
- CLI fecha graciosamente
- Não lança exceção

**Prioridade:** 🟡 Alta

---

### 3.4 Comandos (commands.py)

#### TC-CMD-001: /status
**Esperado:**
- Exibe workspace, goal, modo, checkpoint
- Formato legible

**Prioridade:** 🟡 Alta

---

#### TC-CMD-002: /agent IMPLEMENTER
**Esperado:**
- Modo alterado para IMPLEMENTER
- Estado salvo
- Confirmação exibida

**Prioridade:** 🟡 Alta

---

#### TC-CMD-003: /agent MODO_INVALIDO
**Esperado:**
- Mensagem de erro
- Lista modos válidos

**Prioridade:** 🟠 Média

---

#### TC-CMD-004: /workspace PATH_INVALIDO
**Esperado:**
- Mensagem de erro
- Workspace não alterado

**Prioridade:** 🟠 Média

---

#### TC-CMD-005: /dry-run on/off
**Esperado:**
- Flag alterada no estado
- Mensagem de confirmação

**Prioridade:** 🟠 Média

---

#### TC-CMD-006: /help
**Esperado:**
- Lista todos comandos
- Descrições claras
- Exemplos mostrados

**Prioridade:** 🟡 Alta

---

### 3.5 Edge Cases e Ataques

#### TC-EDGE-001: Path Traversal
**Input:** `../../../etc/passwd`
**Esperado:** Rejeitado com segurança
**Prioridade:** 🔴 Crítica (Segurança)

---

#### TC-EDGE-002: SQL Injection (JSON)
**Input:** `'; DROP TABLE users--`
**Esperado:** Tratado como string normal
**Prioridade:** 🔴 Crítica (Segurança)

---

#### TC-EDGE-003: Comando Gigante (10MB)
**Input:** String de 10MB
**Esperado:** Rejeitado ou truncado
**Prioridade:** 🟠 Média

---

#### TC-EDGE-004: Unicode Mal-formado
**Input:** Bytes inválidos UTF-8
**Esperado:** Erro tratado graciosamente
**Prioridade:** 🟠 Média

---

#### TC-EDGE-005: Disco Cheio
**Simulação:** Sem espaço para salvar state.json
**Esperado:** Erro capturado e reportado
**Prioridade:** 🟡 Alta

---

#### TC-EDGE-006: Permissões Insuficientes
**Simulação:** Pasta read-only
**Esperado:** Erro claro ao usuário
**Prioridade:** 🟡 Alta

---

### 3.6 Performance

#### TC-PERF-001: Inicialização
**Métrica:** Tempo de startup
**Alvo:** < 1 segundo
**Prioridade:** 🟠 Média

---

#### TC-PERF-002: Comando Simples
**Métrica:** Tempo de resposta de /status
**Alvo:** < 100ms
**Prioridade:** 🟠 Média

---

#### TC-PERF-003: Estado Grande (1000 arquivos)
**Métrica:** Tempo para save/load
**Alvo:** < 500ms
**Prioridade:** 🟠 Média

---

#### TC-PERF-004: Memória
**Métrica:** Uso de RAM
**Alvo:** < 100MB
**Prioridade:** 🟠 Média

---

## 4. Critérios de Aceitação {#criterios}

### Must Have (✅ Obrigatório)

1. ☑️ Cobertura de testes ≥ 85%
2. ☑️ Todos os testes críticos (🔴) passando
3. ☑️ Zero erros não tratados
4. ☑️ Estado persiste corretamente
5. ☑️ Checkpoints funcionam 100%
6. ☑️ NLP detecta corretamente 90%+ casos
7. ☑️ Todos comandos / funcionam
8. ☑️ CI passa em todas plataformas

### Should Have (👍 Desejável)

1. Cobertura ≥ 90%
2. Performance dentro dos alvos
3. Testes E2E automatizados
4. Testes de segurança passando

### Nice to Have (⭐ Opcional)

1. Testes de mutação
2. Benchmarks automáticos
3. Testes de carga

---

## 5. Ambientes de Teste {#ambientes}

### Ambiente Local

```bash
python -m pytest tests/ -v
```

### CI/CD (GitHub Actions)

- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Ubuntu, Windows, macOS
- Execução automática em PRs

### Docker (Isolado)

```bash
docker run --rm -v $(pwd):/app python:3.11 \
  bash -c "cd /app && pip install -e . && pytest"
```

---

## 6. Execução dos Testes {#execucao}

### Execução Básica

```bash
pytest tests/
```

### Com Cobertura

```bash
pytest tests/ --cov=perplexity_cli --cov-report=html
```

### Testes Específicos

```bash
# Apenas testes críticos
pytest tests/ -m critical

# Apenas testes de estado
pytest tests/test_state.py -v

# Apenas testes de NLP
pytest tests/test_nlp.py -v
```

### Testes Contínuos (Watch Mode)

```bash
ptw tests/ -- -v
```

### Relatório Completo

```bash
pytest tests/ \
  --cov=perplexity_cli \
  --cov-report=html \
  --cov-report=term \
  --html=report.html \
  --self-contained-html
```

---

## 7. Checklist de Validação Final

Antes de considerar o sistema "pronto para produção":

- [ ] Todos os 60+ casos de teste implementados
- [ ] Cobertura de código ≥ 85%
- [ ] Zero falhas em testes críticos
- [ ] CI verde em todas plataformas
- [ ] Testes de segurança passando
- [ ] Performance dentro dos alvos
- [ ] Documentação de testes completa
- [ ] Casos de uso reais validados
- [ ] Beta testers aprovaram
- [ ] Zero bugs conhecidos de severidade alta

---

## 8. Manutenção

### Quando Adicionar Novos Testes

1. Toda nova feature deve ter testes
2. Todo bug corrigido deve ter teste de regressão
3. Antes de release, executar suite completa

### Revisão Periódica

- **Semanal:** Executar suite completa
- **Mensal:** Revisar cobertura e adicionar testes
- **Release:** Validação completa + testes manuais

---

**🎯 Meta Final:** Zero bugs em produção, 100% de confiança no sistema.
