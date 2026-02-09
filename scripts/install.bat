@echo off
REM Script de instalação para Windows

echo === Instalando Perplexity Agent CLI ===
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python nao encontrado
    echo Instale Python 3.8+ de https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version

REM Criar venv se não existir
if not exist "venv" (
    echo.
    echo Criando ambiente virtual...
    python -m venv venv
)

echo [OK] Ambiente virtual pronto

REM Ativar venv e instalar
echo.
echo Ativando ambiente e instalando dependencias...
call venv\Scripts\activate.bat

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar projeto
pip install -e .

echo.
echo [OK] Instalacao concluida!
echo.
echo Para usar o CLI:
echo   1. Ative o ambiente: venv\Scripts\activate.bat
echo   2. Execute: perplexity-cli
echo.
echo Para ver ajuda: perplexity-cli --help
echo.
pause
