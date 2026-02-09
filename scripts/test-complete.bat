@echo off
REM Script completo de testes para Windows

echo ====================================
echo   SUITE COMPLETA DE TESTES
echo ====================================
echo.

REM Ativar ambiente virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM 1. Unit tests
echo [1/6] Executando testes unitarios...
pytest tests\ -v --tb=short
if errorlevel 1 (
    echo [ERRO] Testes unitarios falharam
    exit /b 1
)
echo [OK] Testes unitarios passaram
echo.

REM 2. Cobertura
echo [2/6] Calculando cobertura...
pytest tests\ --cov=perplexity_cli --cov-report=term --cov-report=html
if errorlevel 1 (
    echo [AVISO] Cobertura baixa
)
echo [OK] Cobertura calculada
echo.

REM 3. Linting
echo [3/6] Executando linters...
flake8 perplexity_cli --max-line-length=120 --ignore=E203,W503
if errorlevel 1 (
    echo [AVISO] Linting com problemas
)
echo [OK] Linting completo
echo.

REM 4. Type checking
echo [4/6] Verificando tipos...
mypy perplexity_cli --ignore-missing-imports
echo [OK] Type checking completo
echo.

REM 5. Testes de seguranca
echo [5/6] Executando testes de seguranca...
pytest tests\test_edge_cases.py::TestSecurityEdgeCases -v
if errorlevel 1 (
    echo [ERRO] Testes de seguranca falharam
    exit /b 1
)
echo [OK] Testes de seguranca passaram
echo.

REM 6. Testes de NLP
echo [6/6] Executando testes de NLP...
pytest tests\test_nlp_complete.py -v
if errorlevel 1 (
    echo [ERRO] Testes de NLP falharam
    exit /b 1
)
echo [OK] Testes de NLP passaram
echo.

echo ====================================
echo   TODOS OS TESTES PASSARAM
echo ====================================
echo.
echo Relatorios gerados:
echo   - Cobertura HTML: htmlcov\index.html
echo.
pause
