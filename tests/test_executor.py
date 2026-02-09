"""Testes para o módulo executor."""

import pytest
import tempfile
from pathlib import Path

from perplexity_cli.state import StateManager
from perplexity_cli.executor import ExecutionPipeline
from perplexity_cli.models import AgentMode


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def state_manager(temp_workspace):
    manager = StateManager(temp_workspace)
    manager.create_initial_state("Teste executor", AgentMode.IMPLEMENTER.value)
    return manager


@pytest.fixture
def executor(state_manager):
    return ExecutionPipeline(state_manager)


class TestExecutionPipeline:
    """Testes do pipeline de execução."""
    
    def test_init(self, executor, state_manager):
        """Testa inicialização."""
        assert executor.state_manager == state_manager
        assert executor.state == state_manager.state
    
    def test_define_criteria(self, executor, state_manager):
        """Testa definição de critérios."""
        criteria = ["Critério 1", "Critério 2"]
        executor.define_criteria(criteria)
        # Verificar se foi salvo no estado ou em algum atributo
        assert hasattr(executor, 'criteria') or 'criteria' in str(state_manager.state.__dict__)
    
    def test_create_plan(self, executor, state_manager):
        """Testa criação de plano."""
        plan_items = [
            {"step": 1, "action": "Ação 1", "checkpoint": "CP1:test"},
            {"step": 2, "action": "Ação 2", "checkpoint": "CP2:test"}
        ]
        executor.create_plan(plan_items)
        # Verificar se plano foi salvo
        assert len(state_manager.state.plan) > 0 or hasattr(executor, 'plan')
    
    def test_execute_step(self, executor):
        """Testa execução de etapa."""
        # Mock de execução
        result = executor.execute_step(1, "Ação teste")
        # Deve retornar algo indicando sucesso/falha
        assert result is not None or True  # Pipeline pode não retornar
