# Script de instalação PowerShell para Windows

Write-Host "=== Instalando Perplexity Agent CLI ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python não encontrado" -ForegroundColor Red
    Write-Host "Instale Python 3.8+ de https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Criar venv se não existir
if (-not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "[OK] Ambiente virtual pronto" -ForegroundColor Green

# Ativar venv
Write-Host ""
Write-Host "Ativando ambiente..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Atualizar pip
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null

# Instalar projeto
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -e .

Write-Host ""
Write-Host "[OK] Instalação concluída!" -ForegroundColor Green
Write-Host ""
Write-Host "Para usar o CLI:" -ForegroundColor Cyan
Write-Host "  1. Ative o ambiente: .\venv\Scripts\Activate.ps1"
Write-Host "  2. Execute: perplexity-cli"
Write-Host ""
Write-Host "Para ver ajuda: perplexity-cli --help"
Write-Host ""
