# 🪟 Instalação no Windows

Guia específico para usuários Windows.

## ⚡ Instalação Rápida

### Opção 1: PowerShell (Recomendado)

```powershell
# 1. Clone o repositório
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli

# 2. Execute o script de instalação PowerShell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1

# 3. Ative o ambiente
.\venv\Scripts\Activate.ps1

# 4. Teste
perplexity-cli --version
```

### Opção 2: Prompt de Comando (.bat)

```cmd
# 1. Clone o repositório
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli

# 2. Execute o script batch
scripts\install.bat

# 3. Ative o ambiente
venv\Scripts\activate.bat

# 4. Teste
perplexity-cli --version
```

## 📋 Pré-requisitos

### 1. Python 3.8+

**Verificar se já tem:**
```powershell
python --version
```

**Se não tiver, instale:**
- Baixe de: https://www.python.org/downloads/
- ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante instalação

### 2. Git (opcional, mas recomendado)

**Verificar:**
```powershell
git --version
```

**Se não tiver:**
- Baixe de: https://git-scm.com/download/win
- Ou use GitHub Desktop: https://desktop.github.com/

## 🛠️ Instalação Manual Passo a Passo

Se os scripts não funcionarem:

### PowerShell

```powershell
# 1. Navegar para a pasta
cd C:\Users\SeuUsuario\Documents\perplexity-agent-cli

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente
.\venv\Scripts\Activate.ps1

# Se der erro de ExecutionPolicy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Depois tente ativar novamente

# 4. Atualizar pip
python -m pip install --upgrade pip

# 5. Instalar projeto
pip install -e .

# 6. Testar
perplexity-cli --version
```

### Prompt de Comando (CMD)

```cmd
# 1. Navegar para a pasta
cd C:\Users\SeuUsuario\Documents\perplexity-agent-cli

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente
venv\Scripts\activate.bat

# 4. Atualizar pip
python -m pip install --upgrade pip

# 5. Instalar projeto
pip install -e .

# 6. Testar
perplexity-cli --version
```

## 🚀 Primeiro Uso

### PowerShell

```powershell
# Ativar ambiente (sempre necessário)
.\venv\Scripts\Activate.ps1

# Executar CLI
perplexity-cli

# Ou com objetivo definido
perplexity-cli --goal "Criar API REST" --mode ARCHITECT
```

### CMD

```cmd
# Ativar ambiente
venv\Scripts\activate.bat

# Executar CLI
perplexity-cli
```

## ⚙️ Desenvolvimento no Windows

### Setup do ambiente de dev

**PowerShell:**
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev-setup.ps1
```

**CMD:**
```cmd
scripts\dev-setup.bat
```

### Executar testes

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
pytest tests\ -v
```

**CMD:**
```cmd
venv\Scripts\activate.bat
pytest tests\ -v
```

## ❗ Problemas Comuns

### Erro: "Execution Policy"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "python não é reconhecido"

**Solução:**
1. Reinstale Python marcando "Add to PATH"
2. Ou adicione manualmente:
   - Painel de Controle → Sistema → Configurações Avançadas
   - Variáveis de Ambiente
   - Adicione `C:\Python3X` e `C:\Python3X\Scripts` ao PATH

### Erro: "pip não é reconhecido"

```powershell
python -m pip --version
# Se funcionar, use sempre: python -m pip install
```

### Erro ao ativar venv no PowerShell

```powershell
# Permitir scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Criar novo venv
Remove-Item -Recurse -Force venv
python -m venv venv

# Ativar
.\venv\Scripts\Activate.ps1
```

### Ambiente não ativa (sem erro)

Verifique se o prompt mudou para mostrar `(venv)`:

```powershell
# Antes
PS C:\Users\victor\Documents\perplexity-agent-cli>

# Depois de ativar
(venv) PS C:\Users\victor\Documents\perplexity-agent-cli>
```

## 🔧 Comandos Windows vs Linux

| Linux/Mac | Windows PowerShell | Windows CMD |
|-----------|-------------------|-------------|
| `source venv/bin/activate` | `.\venv\Scripts\Activate.ps1` | `venv\Scripts\activate.bat` |
| `chmod +x script.sh` | (não necessário) | (não necessário) |
| `./script.sh` | `.\script.ps1` | `script.bat` |
| `ls` | `ls` ou `dir` | `dir` |
| `cat file.txt` | `Get-Content file.txt` | `type file.txt` |
| `rm -rf folder` | `Remove-Item -Recurse folder` | `rmdir /s folder` |

## 📝 Aliases Úteis (PowerShell)

Adicione ao seu perfil PowerShell (`$PROFILE`):

```powershell
# Ativar ambiente rapidamente
function plex-activate {
    .\venv\Scripts\Activate.ps1
}

# Executar CLI
function plex {
    perplexity-cli $args
}

# Rodar testes
function plex-test {
    pytest tests\ -v
}
```

Depois use:
```powershell
plex-activate
plex --goal "Meu objetivo"
```

## 🎯 Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Git instalado (opcional)
- [ ] Repositório clonado
- [ ] Ambiente virtual criado
- [ ] Ambiente ativado (prompt mostra `(venv)`)
- [ ] Dependências instaladas
- [ ] `perplexity-cli --version` funciona

## 💡 Dicas Windows

### 1. Use Windows Terminal

Mais moderno e com melhor suporte:
- Instale da Microsoft Store: "Windows Terminal"
- Suporta abas, temas, e melhor renderização

### 2. Use PowerShell 7+

Versão mais recente:
```powershell
winget install Microsoft.PowerShell
```

### 3. Editor Recomendado

- **VS Code**: Melhor integração Python
- **PyCharm**: IDE completa

### 4. Git no Windows

**Git Bash** (vem com Git for Windows):
- Permite usar comandos Linux
- Melhor para seguir tutoriais Unix

## 🆘 Suporte

Se ainda tiver problemas:

1. **Verifique issues conhecidos**: 
   https://github.com/VictorMoraesSantos/perplexity-agent-cli/issues

2. **Abra uma issue** incluindo:
   - Versão do Windows (`winver`)
   - Versão do Python (`python --version`)
   - Shell usado (PowerShell/CMD)
   - Mensagem de erro completa
   - Passos para reproduzir

3. **Discussões**: 
   https://github.com/VictorMoraesSantos/perplexity-agent-cli/discussions

---

**Desenvolvido para Perplexity** 🔮 | **Por Victor Moraes** 🚀
