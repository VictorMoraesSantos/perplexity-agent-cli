@echo off
REM Setup de ambiente de desenvolvimento para Windows

echo === Setup de Desenvolvimento ===
echo.

REM Ativar venv
call venv\Scripts\activate.bat

REM Instalar modo editável
echo Instalando projeto em modo editavel...
pip install -e .

REM Instalar ferramentas de desenvolvimento
echo.
echo Instalando ferramentas de desenvolvimento...
pip install pytest pytest-cov black flake8 isort mypy

echo.
echo [OK] Setup completo!
echo.
echo Comandos disponiveis:
echo   pytest                  - Executar testes
echo   pytest --cov            - Testes com cobertura
echo   black perplexity_cli    - Formatar codigo
echo   flake8 perplexity_cli   - Lint
echo   isort perplexity_cli    - Ordenar imports
echo.
pause
