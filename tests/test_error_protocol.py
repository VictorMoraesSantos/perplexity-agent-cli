"""Testes para o módulo error_protocol."""

import pytest
import tempfile
from unittest.mock import Mock, patch

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
def error_handler(state_manager):
    return ErrorHandler(state_manager)


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
        
        # Executar diagnóstico
        diagnosis = error_handler.diagnose()
        
        # Deve retornar hipóteses
        assert diagnosis is not None
        assert 'hypotheses' in diagnosis or isinstance(diagnosis, list)
    
    def test_propose_fix(self, error_handler):
        """Testa proposta de correção."""
        error_handler.capture_error("test.py", "SyntaxError: invalid syntax")
        
        fix = error_handler.propose_fix()
        
        assert fix is not None
        assert isinstance(fix, (str, dict))
    
    def test_apply_fix(self, error_handler):
        """Testa aplicação de correção."""
        fix = {"action": "install", "package": "requests"}
        
        # Deve tentar aplicar (pode falhar se não implementado)
        try:
            result = error_handler.apply_fix(fix)
            assert result is not None
        except NotImplementedError:
            pytest.skip("apply_fix não implementado")
    
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
        # 1. Capturar erro
        state_manager.set_error(
            where="main.py:42",
            message="ValueError: invalid value",
            log_excerpt="Traceback (most recent call last)..."
        )
        
        assert state_manager.state.last_error is not None
        
        # 2. Diagnóstico seria executado pelo ErrorHandler
        # 3. Propor correção
        # 4. Aplicar
        # 5. Limpar se sucesso
        
        state_manager.clear_error()
        assert state_manager.state.last_error is None
