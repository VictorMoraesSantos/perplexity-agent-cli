"""Testes do sistema de estado."""

import pytest
import tempfile
import os
from pathlib import Path
from perplexity_cli.state import StateManager
from perplexity_cli.models import AgentMode


def test_state_creation():
    """Testa criação de estado inicial."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StateManager(tmpdir)
        state = manager.create_initial_state("Testar sistema", AgentMode.ARCHITECT.value)
        
        assert state.goal == "Testar sistema"
        assert state.agent_mode == AgentMode.ARCHITECT.value
        assert state.workspace == tmpdir
        assert state.current_checkpoint == "CP0:init"


def test_state_persistence():
    """Testa persistência de estado em JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StateManager(tmpdir)
        original = manager.create_initial_state("Teste persistência")
        
        # Salvar
        manager.save()
        
        # Criar novo manager e carregar
        manager2 = StateManager(tmpdir)
        loaded = manager2.load()
        
        assert loaded is not None
        assert loaded.goal == original.goal
        assert loaded.agent_mode == original.agent_mode


def test_checkpoint_update():
    """Testa atualização de checkpoint."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StateManager(tmpdir)
        manager.create_initial_state("Teste checkpoint")
        
        manager.update_checkpoint("CP1:test-complete")
        
        assert manager.state.current_checkpoint == "CP1:test-complete"
        assert manager.state.last_successful_checkpoint == "CP1:test-complete"
