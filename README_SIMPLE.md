# Perplexity Agent CLI - Modo Simples

## 🚀 Uso Ultra-Simples

### Instalar

```bash
pip install -e .
```

### Executar

```bash
perplexity-cli
```

### Usar

**Apenas fale o que quer:**

```
⚡ Bem-vindo ao Perplexity Agent CLI

Digite o que você quer fazer e eu executo.

Workspace: /caminho/do/projeto

Você: criar uma API REST em Python

→ Modo: IMPLEMENTER
→ Objetivo: Criar uma API REST em Python

⏳ Executando...

1. Analisando workspace...
2. Criando plano...
3. Executando etapas...

✓ Concluído!

Próximos passos sugeridos:
  1. Adicionar testes
  2. Revisar código implementado
  3. Documentar funcionalidades

Você: adicionar testes

→ Modo: IMPLEMENTER
→ Objetivo: Adicionar testes

⏳ Executando...
...

Você: sair

Até logo! 👋
```

---

## ✨ Características

### **Zero Comandos**
Sem `/agent`, `/status`, `/plan` - apenas converse

### **Execução Automática**
Você fala, ele executa. Simples assim.

### **Detecção Inteligente**
Detecta automaticamente:
- 🏛️ **ARCHITECT** - "estruturar projeto", "planejar arquitetura"
- 🛠️ **IMPLEMENTER** - "criar API", "adicionar feature"
- 🐛 **DEBUGGER** - "corrigir bug", "erro no arquivo"
- ✅ **REVIEWER** - "revisar código", "verificar qualidade"
- 📝 **DOCUMENTER** - "documentar", "criar README"
- 🚀 **OPS** - "configurar CI/CD", "criar Docker"

### **Sugestões Automáticas**
Após cada tarefa, sugere próximos passos

---

## 🎯 Exemplos Rápidos

### Criar projeto do zero

```
Você: estruturar um projeto Python com Flask
[agente executa]

Você: criar endpoint de usuários
[agente executa]

Você: adicionar testes
[agente executa]

Você: documentar a API
[agente executa]

Você: configurar CI/CD
[agente executa]
```

### Corrigir bugs

```
Você: corrigir erro no arquivo auth.py linha 42
[agente analisa e corrige]

Você: testar a correção
[agente executa testes]
```

### Melhorar código

```
Você: revisar o código do módulo de autenticação
[agente revisa e sugere melhorias]

Você: aplicar melhorias
[agente refatora]
```

---

## 🆚🆆 vs Modo Avançado

### Modo Simples (padrão)
```bash
perplexity-cli
```
✅ Interface conversacional pura  
✅ Execução automática  
✅ Zero comandos complexos  
🎯 **Recomendado para uso diário**

### Modo Avançado
```bash
perplexity-cli-advanced
```
⚙️ Comandos `/` disponíveis  
⚙️ Controle manual de checkpoints  
⚙️ Dry-run mode  
🛠️ Para usuários avançados

---

## ❓ FAQ

**P: Preciso digitar comandos especiais?**  
R: Não! Apenas fale naturalmente.

**P: Como escolho o modo (ARCHITECT, IMPLEMENTER, etc.)?**  
R: Automático! O agente detecta pela sua frase.

**P: Ele realmente executa ou só sugere?**  
R: Executa automaticamente! (modo simulação por enquanto)

**P: Como sair?**  
R: Digite `sair`, `exit`, `quit` ou `Ctrl+C`

**P: E se eu quiser mais controle?**  
R: Use `perplexity-cli-advanced` para modo avançado

---

## 🚀 Começar Agora

```bash
# 1. Instalar
pip install -e .

# 2. Executar
perplexity-cli

# 3. Falar o que quer
Você: criar uma API

# 4. Pronto!
```

**Simples assim.** ✨
