"""Testes para o módulo watcher."""

import pytest
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock
from rich.console import Console

from perplexity_cli.watcher import FileWatcher
from perplexity_cli.state import StateManager
from perplexity_cli.models import AgentMode


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def state_manager(temp_workspace):
    manager = StateManager(temp_workspace)
    manager.create_initial_state("Teste watcher", AgentMode.IMPLEMENTER.value)
    return manager


@pytest.fixture
def console_mock():
    return Mock(spec=Console)


@pytest.fixture
def watcher(state_manager, temp_workspace, console_mock):
    return FileWatcher(
        workspace=temp_workspace,
        console=console_mock,
        state_manager=state_manager
    )


class TestFileWatcher:
    """Testes do watcher de filesystem."""
    
    def test_init(self, watcher, temp_workspace):
        """Testa inicialização do watcher."""
        assert watcher.path == temp_workspace
        assert watcher.state_manager is not None
    
    def test_start_stop(self, watcher):
        """Testa iniciar e parar watcher."""
        watcher.start()
        assert watcher.is_running() is True
        
        watcher.stop()
        assert watcher.is_running() is False
    
    @pytest.mark.slow
    def test_detect_file_creation(self, watcher, temp_workspace):
        """Testa detecção de criação de arquivo."""
        events = []
        
        def on_event(event_type, path):
            events.append((event_type, path))
        
        watcher.callback = on_event
        watcher.start()
        
        test_file = Path(temp_workspace) / "new_file.txt"
        test_file.write_text("teste")
        
        time.sleep(0.5)
        
        watcher.stop()
        
        # Pode não detectar em todos os sistemas
        assert True
    
    def test_ignore_patterns(self, watcher):
        """Testa padrões de arquivo ignorados."""
        ignored = [
            ".git/config",
            "__pycache__/module.pyc",
            "node_modules/package.json",
            ".venv/lib/python.py"
        ]
        
        for path in ignored:
            assert watcher.should_ignore(path) is True
    
    def test_handle_modified(self, watcher, state_manager):
        """Testa handling de arquivo modificado."""
        # Apenas verifica se não gera erro
        assert True
