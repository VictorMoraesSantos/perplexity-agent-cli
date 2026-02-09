# 🚀 Quickstart - Perplexity Agent CLI

Guia prático para começar em 5 minutos.

## Instalação

### Opção 1: Instalação Automática (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli

# Execute o script de instalação
chmod +x scripts/install.sh
./scripts/install.sh

# Ative o ambiente
source venv/bin/activate
```

### Opção 2: Instalação Manual

```bash
# Clone e entre na pasta
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale
pip install -e .
```

### Opção 3: Via pip (quando publicado)

```bash
pip install perplexity-agent-cli
```

## Primeiro Uso

### 1. Iniciar CLI Interativo

```bash
perplexity-cli
```

Você verá:

```
╭────────────────────────────────────╮
│  🤖 Perplexity Agent CLI          │
│  Sistema com checkpoints           │
╰────────────────────────────────────╯

Qual é o objetivo desta sessão? _
```

### 2. Definir Objetivo

```
Qual é o objetivo desta sessão? Criar sistema de autenticação
```

### 3. Usar Comandos

```bash
[ARCHITECT] > /status      # Ver estado atual
[ARCHITECT] > /plan        # Ver plano
[ARCHITECT] > /workspace /caminho/projeto  # Mudar workspace
```

## Exemplo Prático Completo

### Cenário: Adicionar Testes a um Projeto

```bash
# 1. Iniciar com objetivo definido
perplexity-cli --goal "Adicionar testes unitários" --mode IMPLEMENTER

# 2. Verificar workspace
[IMPLEMENTER] > /workspace
📁 Workspace atual: /home/user/meu-projeto

# 3. Ver plano gerado
[IMPLEMENTER] > /plan

# 4. Ativar modo dry-run para simular
[IMPLEMENTER] > /dry-run on
[DRY-RUN] Modo simulação ativado

# 5. Executar ações (simuladas)
# ... agente trabalha ...

# 6. Revisar o que seria feito
[IMPLEMENTER] > /status

# 7. Aplicar mudanças reais
[IMPLEMENTER] > /dry-run off
[IMPLEMENTER] > /apply

# 8. Trocar para revisor
[IMPLEMENTER] > /agent REVIEWER
✓ Modo alterado: REVIEWER

# 9. Revisar trabalho
[REVIEWER] > /status
# ... revisar código ...

# 10. Sair
[REVIEWER] > /exit
```

## Comandos Essenciais

| Comando | O que faz | Exemplo |
|---------|-----------|----------|
| `/agent MODO` | Troca perfil do agente | `/agent DEBUGGER` |
| `/status` | Mostra estado completo | `/status` |
| `/plan` | Exibe plano atual | `/plan` |
| `/workspace PATH` | Muda diretório | `/workspace ~/projeto` |
| `/dry-run on` | Ativa simulação | `/dry-run on` |
| `/watch on` | Liga monitor de arquivos | `/watch on` |
| `/resume` | Retoma de checkpoint | `/resume` |
| `/help` | Ajuda completa | `/help` |

## 6 Modos de Agente

### 🏛️ ARCHITECT
**Quando usar:** Planejamento, estrutura, arquitetura

```bash
/agent ARCHITECT
```

Exemplo: "Definir estrutura de microserviços"

### 🛠️ IMPLEMENTER
**Quando usar:** Codificar, implementar features

```bash
/agent IMPLEMENTER
```

Exemplo: "Implementar endpoint de login"

### 🔍 DEBUGGER
**Quando usar:** Investigar bugs, corrigir erros

```bash
/agent DEBUGGER
```

Exemplo: "Corrigir erro de autenticação"

### ✅ REVIEWER
**Quando usar:** Revisar código, qualidade

```bash
/agent REVIEWER
```

Exemplo: "Revisar PR #42"

### 📝 DOCUMENTER
**Quando usar:** Escrever docs, READMEs

```bash
/agent DOCUMENTER
```

Exemplo: "Documentar API REST"

### ⚙️ OPS
**Quando usar:** CI/CD, Docker, deploy

```bash
/agent OPS
```

Exemplo: "Configurar GitHub Actions"

## Entendendo Checkpoints

Checkpoints são pontos de salvamento automáticos:

```json
{
  "current_checkpoint": "CP2:implementation-done",
  "last_successful_checkpoint": "CP2:implementation-done"
}
```

### Se algo der errado:

```bash
/resume
```

O agente retorna exatamente ao último checkpoint válido.

## Sistema de Estado

Todo progresso é salvo em `.perplexity-cli/state.json`:

```bash
# Ver estado completo
/status

# Estado é salvo automaticamente a cada checkpoint
# Você pode retomar mesmo após fechar o CLI
```

## Modo Dry-Run (Simulação)

**SEMPRE** teste antes com dry-run:

```bash
# 1. Ativar
/dry-run on

# 2. Executar ações (simuladas)
# Nenhum arquivo é modificado

# 3. Revisar o que seria feito
/status

# 4. Se OK, aplicar para valer
/dry-run off
/apply
```

## Watcher de Arquivos

Monitora mudanças externas:

```bash
# Ligar watcher
/watch on

# Agora se você editar arquivos externamente,
# o agente detecta e atualiza o contexto
```

**Arquivos ignorados:**
- `.git/`
- `__pycache__/`
- `node_modules/`
- `.venv/`

## Protocolo de Erro

Quando algo falha:

```
✗ ERRO DETECTADO
Local: src/main.py:42
Mensagem: ImportError: No module named 'requests'

Executando diagnóstico automático...
  1. Analisando stacktrace...
  2. Verificando dependências...

Hipóteses:
1. [HIGH] Dependência não instalada
2. [MEDIUM] Ambiente virtual incorreto

Aplicando correção...
```

O agente:
1. Captura erro
2. Executa 2 diagnósticos automáticos
3. Propõe hipóteses
4. Aplica correção mínima
5. Se falhar, pede ajuda

## Dicas Práticas

### ✅ Boas Práticas

1. **Sempre use dry-run primeiro**
   ```bash
   /dry-run on
   ```

2. **Verifique o plano antes**
   ```bash
   /plan
   ```

3. **Troque de agente conforme necessário**
   ```bash
   /agent IMPLEMENTER  # para codificar
   /agent REVIEWER     # para revisar
   ```

4. **Use /status frequentemente**
   ```bash
   /status
   ```

5. **Ative watcher para projetos ativos**
   ```bash
   /watch on
   ```

### ❌ O que Evitar

1. Não aplique mudanças sem dry-run
2. Não ignore erros - use /resume
3. Não mude workspace no meio de tarefa
4. Não pule checkpoints

## Casos de Uso Comuns

### Adicionar Feature

```bash
perplexity-cli --goal "Adicionar autenticação OAuth" --mode ARCHITECT
# 1. ARCHITECT define estrutura
# 2. Troca para IMPLEMENTER
/agent IMPLEMENTER
# 3. IMPLEMENTER codifica
# 4. Troca para REVIEWER
/agent REVIEWER
# 5. REVIEWER verifica
```

### Corrigir Bug

```bash
perplexity-cli --goal "Corrigir erro 500 no endpoint /api/users" --mode DEBUGGER
# DEBUGGER investiga, propõe hipóteses e corrige
```

### Documentar Projeto

```bash
perplexity-cli --goal "Atualizar README e docs da API" --mode DOCUMENTER
# DOCUMENTER escreve docs, exemplos e atualiza README
```

### Setup CI/CD

```bash
perplexity-cli --goal "Configurar GitHub Actions com testes" --mode OPS
# OPS cria workflows, Dockerfiles e scripts
```

## Troubleshooting

### Problema: "Comando não encontrado: perplexity-cli"

**Solução:**
```bash
source venv/bin/activate
pip install -e .
```

### Problema: Estado corrompido

**Solução:**
```bash
rm .perplexity-cli/state.json
perplexity-cli  # Reinicia
```

### Problema: Watcher não funciona

**Solução:**
```bash
pip install --upgrade watchdog
```

## Próximos Passos

1. **Leia o README completo**: [README.md](README.md)
2. **Veja exemplos**: pasta `examples/`
3. **Execute testes**: `make test`
4. **Contribua**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Recursos Adicionais

- **Documentação Completa**: [README.md](README.md)
- **Exemplos de Código**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/VictorMoraesSantos/perplexity-agent-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/VictorMoraesSantos/perplexity-agent-cli/discussions)

## Suporte

Precisa de ajuda?

1. `/help` no CLI
2. Leia [README.md](README.md)
3. Abra uma [Issue](https://github.com/VictorMoraesSantos/perplexity-agent-cli/issues)
4. Participe das [Discussions](https://github.com/VictorMoraesSantos/perplexity-agent-cli/discussions)

---

**Desenvolvido para Perplexity** 🔮 | **Por Victor Moraes** 🚀
