# 🚀 Quick Start - Perplexity Agent CLI

## Instalação

```bash
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli
pip install -e .
```

## Uso Imediato

### 1. Iniciar

```bash
perplexity-cli
```

### 2. Conversar

Agora é só falar o que você quer:

```
⚡ Sessão Iniciada

Modo: AUTO
Workspace: C:\Users\victor\Documents\projeto

[AUTO] > criar uma API REST em Python

→ Modo: IMPLEMENTER
→ Objetivo: Criar uma API REST em Python

⏳ Executando automaticamente...

1. Analisando workspace...
2. Criando plano...
3. Executando etapas...

✓ Execução concluída!

Sugestões:
  1. Adicionar testes
  2. Documentar código

[AUTO] > adicionar testes para a API

→ Modo: IMPLEMENTER
→ Objetivo: Adicionar testes para a API

⏳ Executando automaticamente...
...

[AUTO] > revisar o código

→ Modo: REVIEWER
→ Objetivo: Revisar o código

⏳ Executando automaticamente...
...

[AUTO] > sair

Até logo! 👋
```

## ✨ Exemplos Rápidos

### Criar projeto

```
[AUTO] > estruturar projeto Flask com autenticação
```

### Adicionar features

```
[AUTO] > criar endpoint de usuários com CRUD
[AUTO] > adicionar validação de dados
[AUTO] > implementar middleware de auth
```

### Corrigir bugs

```
[AUTO] > corrigir erro no arquivo auth.py linha 42
[AUTO] > investigar crash no módulo database
```

### Melhorar código

```
[AUTO] > revisar função process_data
[AUTO] > refatorar classe UserController
```

### Documentar

```
[AUTO] > documentar a API com exemplos
[AUTO] > criar README completo
[AUTO] > adicionar docstrings nos módulos
```

### Configurar infra

```
[AUTO] > configurar GitHub Actions para CI
[AUTO] > criar Dockerfile
[AUTO] > setup de pre-commit hooks
```

## 🎯 Modos Disponíveis (Automáticos)

O agente detecta automaticamente o modo baseado no que você fala:

| Modo | Palavras-chave | Exemplos |
|------|---------------|----------|
| **ARCHITECT** | estruturar, arquitetura, planejar | "estruturar projeto", "definir arquitetura" |
| **IMPLEMENTER** | criar, adicionar, implementar | "criar API", "adicionar testes" |
| **DEBUGGER** | corrigir, bug, erro, problema | "corrigir erro", "debugar crash" |
| **REVIEWER** | revisar, analisar, verificar | "revisar código", "verificar qualidade" |
| **DOCUMENTER** | documentar, readme, docs | "documentar API", "criar README" |
| **OPS** | deploy, ci/cd, docker | "configurar CI", "criar Dockerfile" |

## 🛠️ Comandos Especiais

Se precisar de controle manual:

```bash
/status         # Ver estado atual
/plan           # Ver plano de execução
/agent MODO     # Forçar modo específico
/workspace PATH # Trocar workspace
/auto off       # Desativar execução automática
/auto on        # Reativar execução automática
/help           # Ajuda completa
sair            # Sair
```

## ❓ FAQ

**P: Ele realmente executa ou só simula?**  
R: Por padrão executa! Use `/dry-run on` para simular primeiro.

**P: Como escolher o modo?**  
R: Automático! Basta falar naturalmente.

**P: Posso desativar a execução automática?**  
R: Sim! Use `/auto off` ou inicie com `perplexity-cli --no-auto`

**P: Como sair?**  
R: Digite `sair`, `exit`, `quit` ou pressione `Ctrl+C`

**P: Dá para usar em qualquer projeto?**  
R: Sim! Ele se adapta ao workspace que você especificar.

## 💡 Dicas

1. **Seja específico**: "criar endpoint de login" é melhor que "fazer autenticação"
2. **Iterativo**: Faça em pequenos passos
3. **Use sugestões**: Após cada execução, veja as sugestões de próximos passos
4. **Revise sempre**: Após implementar, use "revisar o código"

## 🚀 Workflow Recomendado

```bash
# 1. Planejar
[AUTO] > estruturar projeto Python com Flask

# 2. Implementar
[AUTO] > criar endpoint de usuários
[AUTO] > adicionar validação
[AUTO] > implementar autenticação

# 3. Testar
[AUTO] > adicionar testes unitários
[AUTO] > adicionar testes de integração

# 4. Revisar
[AUTO] > revisar qualidade do código

# 5. Documentar
[AUTO] > documentar endpoints da API
[AUTO] > criar README

# 6. Configurar
[AUTO] > configurar CI/CD
[AUTO] > criar Dockerfile
```

## 🔗 Links Úteis

- [README Completo](README.md) - Documentação detalhada
- [Guia de Testes](TESTING.md) - Como rodar testes
- [Guia Windows](INSTALL_WINDOWS.md) - Instalação no Windows

---

**Pronto para começar?**

```bash
perplexity-cli
```

**Apenas fale o que quer fazer!** ✨
