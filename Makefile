.PHONY: help install dev test lint format clean build

help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instalar pacote"
	@echo "  make dev        - Setup ambiente de desenvolvimento"
	@echo "  make test       - Executar testes"
	@echo "  make lint       - Executar linters"
	@echo "  make format     - Formatar código"
	@echo "  make clean      - Limpar arquivos temporários"
	@echo "  make build      - Build do pacote"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=perplexity_cli --cov-report=term --cov-report=html

lint:
	flake8 perplexity_cli
	mypy perplexity_cli --ignore-missing-imports

format:
	black perplexity_cli tests examples
	isort perplexity_cli tests examples

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

build:
	python -m build

run:
	perplexity-cli
