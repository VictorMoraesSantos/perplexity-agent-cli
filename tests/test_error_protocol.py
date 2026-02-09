"""Testes para o módulo error_protocol."""

import pytest
import tempfile
from unittest.mock import Mock, patch
from rich.console import Console

from perplexity_cli.state import StateManager, RunState
from perplexity_cli.error_protocol import ErrorProtocol, ErrorHandler
from perplexity_cli.models import AgentMode


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def state_manager(temp_workspace):
    manager = StateManager(temp_workspace)
    manager.create_initial_state("Teste erro", AgentMode.DEBUGGER.value)
    return manager


@pytest.fixture
def console_mock():
    return Mock(spec=Console)


@pytest.fixture
def error_handler(state_manager, console_mock):
    return ErrorHandler(state_manager, console_mock)


class TestErrorHandler:
    """Testes do handler de erros."""
    
    def test_capture_error(self, error_handler, state_manager):
        """Testa captura de erro."""
        error_handler.capture_error(
            where="test.py:10",
            message="Erro de teste",
            log_excerpt="Traceback..."
        )
        assert state_manager.state.last_error is not None
        assert "test.py" in state_manager.state.last_error['where']
    
    def test_diagnose_error(self, error_handler):
        """Testa diagnóstico de erro."""
        error_handler.capture_error("test.py", "ImportError: No module named 'requests'")
        
        diagnosis = error_handler.diagnose()
        
        assert diagnosis is not None
        assert 'hypotheses' in diagnosis
    
    def test_propose_fix(self, error_handler):
        """Testa proposta de correção."""
        error_handler.capture_error("test.py", "SyntaxError: invalid syntax")
        
        fix = error_handler.propose_fix()
        
        assert fix is not None
        assert isinstance(fix, dict)
    
    def test_apply_fix(self, error_handler):
        """Testa aplicação de correção."""
        fix = {"action": "install", "package": "requests"}
        
        result = error_handler.apply_fix(fix)
        assert isinstance(result, bool)
    
    def test_clear_error(self, error_handler, state_manager):
        """Testa limpeza de erro."""
        error_handler.capture_error("test.py", "Erro")
        assert state_manager.state.last_error is not None
        
        state_manager.clear_error()
        assert state_manager.state.last_error is None


class TestErrorProtocol:
    """Testes do protocolo de erro."""
    
    def test_error_workflow(self, state_manager):
        """Testa workflow completo de erro."""
        state_manager.set_error(
            where="main.py:42",
            message="ValueError: invalid value",
            log_excerpt="Traceback (most recent call last)..."
        )
        
        assert state_manager.state.last_error is not None
        
        state_manager.clear_error()
        assert state_manager.state.last_error is None
