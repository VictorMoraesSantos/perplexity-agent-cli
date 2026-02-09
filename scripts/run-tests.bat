@echo off
REM Executa testes completos no Windows

echo === Executando Testes ===
echo.

REM Ativar venv
call venv\Scripts\activate.bat

REM Unit tests com coverage
echo [1/3] Unit tests...
echo.
pytest tests\ -v --cov=perplexity_cli --cov-report=term --cov-report=html

echo.
echo [2/3] Linting...
echo.
flake8 perplexity_cli --max-line-length=120 --ignore=E203,W503

echo.
echo [3/3] Type checking...
echo.
mypy perplexity_cli --ignore-missing-imports

echo.
echo [OK] Testes concluidos!
echo Relatorio HTML: htmlcov\index.html
echo.
pause
