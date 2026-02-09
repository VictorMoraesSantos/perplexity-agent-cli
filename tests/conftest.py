"""Configurações globais de testes."""

import pytest
import sys
import os
from pathlib import Path

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Retorna path raiz do projeto."""
    return project_root


@pytest.fixture(autouse=True)
def cleanup_state_files():
    """Limpa arquivos de estado após cada teste."""
    yield
    # Cleanup após teste
    state_dirs = Path(".").rglob(".perplexity-cli")
    for state_dir in state_dirs:
        if state_dir.is_dir():
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)


def pytest_configure(config):
    """Configuração customizada do pytest."""
    config.addinivalue_line(
        "markers", "slow: marca testes lentos que podem ser pulados"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
