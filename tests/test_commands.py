"""Testes completos para o módulo commands."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from rich.console import Console

from perplexity_cli.state import StateManager
from perplexity_cli.commands import CommandHandler
from perplexity_cli.models import AgentMode


@pytest.fixture
def temp_workspace():
    """Cria workspace temporário."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def state_manager(temp_workspace):
    """Cria StateManager com workspace temporário."""
    manager = StateManager(temp_workspace)
    manager.create_initial_state("Teste", AgentMode.ARCHITECT.value)
    return manager


@pytest.fixture
def console_mock():
    """Mock do console."""
    return Mock(spec=Console)


@pytest.fixture
def command_handler(state_manager, console_mock):
    """Cria CommandHandler com deps mockadas."""
    return CommandHandler(state_manager, console_mock)


class TestCommandAgent:
    """Testes do comando /agent."""
    
    def test_change_agent_mode_valid(self, command_handler, state_manager):
        """Testa troca de modo válida."""
        command_handler.cmd_agent("IMPLEMENTER")
        assert state_manager.state.agent_mode == "IMPLEMENTER"
    
    def test_change_agent_mode_invalid(self, command_handler, console_mock):
        """Testa modo inválido."""
        command_handler.cmd_agent("INVALID_MODE")
        # Deve mostrar erro
        assert console_mock.print.called
    
    def test_change_agent_mode_empty(self, command_handler, console_mock):
        """Testa sem argumento."""
        command_handler.cmd_agent("")
        assert console_mock.print.called


class TestCommandWorkspace:
    """Testes do comando /workspace."""
    
    def test_show_current_workspace(self, command_handler, console_mock, temp_workspace):
        """Testa exibição do workspace atual."""
        command_handler.cmd_workspace("")
        assert console_mock.print.called
    
    def test_change_workspace_valid(self, command_handler, state_manager):
        """Testa mudança de workspace válida."""
        with tempfile.TemporaryDirectory() as new_workspace:
            command_handler.cmd_workspace(new_workspace)
            assert state_manager.workspace == new_workspace
    
    def test_change_workspace_invalid(self, command_handler, console_mock):
        """Testa workspace inválido."""
        command_handler.cmd_workspace("/caminho/inexistente")
        assert console_mock.print.called


class TestCommandStatus:
    """Testes do comando /status."""
    
    def test_show_status(self, command_handler, console_mock, state_manager):
        """Testa exibição de status."""
        command_handler.cmd_status("")
        assert console_mock.print.called
    
    def test_status_with_error(self, command_handler, state_manager, console_mock):
        """Testa status com erro registrado."""
        state_manager.set_error("test.py", "Erro de teste")
        command_handler.cmd_status("")
        assert console_mock.print.called


class TestCommandPlan:
    """Testes do comando /plan."""
    
    def test_show_plan_empty(self, command_handler, console_mock):
        """Testa plano vazio."""
        command_handler.cmd_plan("")
        assert console_mock.print.called
    
    def test_show_plan_with_items(self, command_handler, state_manager, console_mock):
        """Testa plano com itens."""
        state_manager.state.plan = ["Item 1", "Item 2"]
        state_manager.save()
        command_handler.cmd_plan("")
        assert console_mock.print.called


class TestCommandDryRun:
    """Testes do comando /dry-run."""
    
    def test_enable_dry_run(self, command_handler, state_manager):
        """Testa ativar dry-run."""
        command_handler.cmd_dry_run("on")
        assert state_manager.state.dry_run is True
    
    def test_disable_dry_run(self, command_handler, state_manager):
        """Testa desativar dry-run."""
        state_manager.state.dry_run = True
        command_handler.cmd_dry_run("off")
        assert state_manager.state.dry_run is False
    
    def test_invalid_arg(self, command_handler, console_mock):
        """Testa argumento inválido."""
        command_handler.cmd_dry_run("maybe")
        assert console_mock.print.called


class TestCommandWatch:
    """Testes do comando /watch."""
    
    def test_enable_watch(self, command_handler, state_manager):
        """Testa ativar watcher."""
        command_handler.cmd_watch("on")
        assert state_manager.state.watch_enabled is True
    
    def test_disable_watch(self, command_handler, state_manager):
        """Testa desativar watcher."""
        state_manager.state.watch_enabled = True
        command_handler.cmd_watch("off")
        assert state_manager.state.watch_enabled is False


class TestCommandHelp:
    """Testes do comando /help."""
    
    def test_show_help(self, command_handler, console_mock):
        """Testa exibição de ajuda."""
        command_handler.cmd_help("")
        assert console_mock.print.called
        # Verifica se mostra comandos principais
        calls = [str(call) for call in console_mock.print.call_args_list]
        help_text = ' '.join(calls)
        assert '/agent' in help_text or 'agent' in help_text.lower()
