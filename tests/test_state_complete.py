"""Testes completos do sistema de estado."""

import pytest
import tempfile
import os
import json
from pathlib import Path
from perplexity_cli.state import StateManager, RunState
from perplexity_cli.models import AgentMode


class TestStateCreation:
    """Testes de criação de estado."""
    
    def test_create_initial_state_default(self):
        """TC-STATE-001: Criação de estado inicial com padrões."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            state = manager.create_initial_state("Teste")
            
            assert state.goal == "Teste"
            assert state.agent_mode == "ARCHITECT"  # Padrão
            assert state.workspace == tmpdir
            assert state.current_checkpoint == "CP0:init"
            assert state.last_successful_checkpoint == "CP0:init"
            assert state.current_plan_step == 0
            assert len(state.files_touched) == 0
            assert len(state.commands_run) == 0
    
    def test_create_initial_state_custom_mode(self):
        """Cria estado com modo customizado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            state = manager.create_initial_state("Teste", agent_mode="DEBUGGER")
            
            assert state.agent_mode == "DEBUGGER"
    
    def test_create_initial_state_custom_workspace(self):
        """Cria estado com workspace customizado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_workspace = "/custom/path"
            manager = StateManager(tmpdir)
            state = manager.create_initial_state("Teste", workspace=custom_workspace)
            
            assert state.workspace == custom_workspace


class TestStatePersistence:
    """Testes de persistência de estado."""
    
    def test_save_and_load(self):
        """TC-STATE-002: Persistência completa de estado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Criar e salvar
            manager1 = StateManager(tmpdir)
            original = manager1.create_initial_state("Teste persistência")
            original.files_touched = ["file1.py", "file2.py"]
            original.current_plan_step = 5
            manager1.save()
            
            # Carregar em novo manager
            manager2 = StateManager(tmpdir)
            loaded = manager2.load()
            
            assert loaded is not None
            assert loaded.goal == original.goal
            assert loaded.agent_mode == original.agent_mode
            assert loaded.workspace == original.workspace
            assert loaded.current_plan_step == original.current_plan_step
            assert loaded.files_touched == original.files_touched
    
    def test_save_creates_directory(self):
        """Salvar cria diretório se não existe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            state = manager.create_initial_state("Teste")
            
            state_dir = Path(tmpdir) / ".perplexity-cli"
            assert state_dir.exists()
            assert state_dir.is_dir()
    
    def test_save_without_state_raises_error(self):
        """Salvar sem estado lança erro."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            
            with pytest.raises(ValueError, match="Nenhum estado disponível"):
                manager.save()
    
    def test_load_nonexistent_returns_none(self):
        """Carregar arquivo inexistente retorna None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            result = manager.load()
            
            assert result is None
    
    def test_load_corrupted_file_returns_none(self):
        """TC-STATE-004: Arquivo corrompido retorna None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            
            # Criar arquivo inválido
            manager.ensure_state_dir()
            with open(manager.state_file, 'w') as f:
                f.write("{ invalid json")
            
            result = manager.load()
            assert result is None
    
    def test_load_empty_file_returns_none(self):
        """Arquivo vazio retorna None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            
            # Criar arquivo vazio
            manager.ensure_state_dir()
            with open(manager.state_file, 'w') as f:
                f.write("")
            
            result = manager.load()
            assert result is None


class TestCheckpointManagement:
    """Testes de gerenciamento de checkpoints."""
    
    def test_update_checkpoint_success(self):
        """TC-STATE-003: Atualização de checkpoint com sucesso."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.update_checkpoint("CP1:test-complete")
            
            assert manager.state.current_checkpoint == "CP1:test-complete"
            assert manager.state.last_successful_checkpoint == "CP1:test-complete"
            assert "CP1:test-complete" in manager.state.checkpoints
            assert manager.state.checkpoints["CP1:test-complete"] is True
    
    def test_update_checkpoint_failure(self):
        """Atualiza checkpoint com falha."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.update_checkpoint("CP1:failed", success=False)
            
            assert manager.state.current_checkpoint == "CP1:failed"
            # last_successful não deve mudar
            assert manager.state.last_successful_checkpoint == "CP0:init"
    
    def test_multiple_checkpoints(self):
        """Múltiplos checkpoints em sequência."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            checkpoints = ["CP1:step1", "CP2:step2", "CP3:step3"]
            for cp in checkpoints:
                manager.update_checkpoint(cp)
            
            assert manager.state.current_checkpoint == "CP3:step3"
            assert manager.state.last_successful_checkpoint == "CP3:step3"
            assert len(manager.state.checkpoints) == 3


class TestCommandHistory:
    """Testes de histórico de comandos."""
    
    def test_add_command(self):
        """Adiciona comando ao histórico."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.add_command("pytest", "ok", "All tests passed")
            
            assert len(manager.state.commands_run) == 1
            cmd = manager.state.commands_run[0]
            assert cmd["cmd"] == "pytest"
            assert cmd["result"] == "ok"
            assert "timestamp" in cmd
    
    def test_add_multiple_commands(self):
        """TC-STATE-005: Múltiplos comandos no histórico."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            # Adicionar 100 comandos
            for i in range(100):
                manager.add_command(f"cmd{i}", "ok", f"output{i}")
            
            assert len(manager.state.commands_run) == 100
            # Verificar ordem
            assert manager.state.commands_run[0]["cmd"] == "cmd0"
            assert manager.state.commands_run[99]["cmd"] == "cmd99"
    
    def test_command_output_truncation(self):
        """Output de comando é truncado em 500 chars."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            long_output = "x" * 1000
            manager.add_command("test", "ok", long_output)
            
            cmd = manager.state.commands_run[0]
            assert len(cmd["output"]) == 500


class TestErrorManagement:
    """Testes de gerenciamento de erros."""
    
    def test_set_error(self):
        """Registra erro no estado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.set_error(
                where="test.py:42",
                message="ImportError",
                log_excerpt="Traceback..."
            )
            
            assert manager.state.last_error is not None
            assert manager.state.last_error["where"] == "test.py:42"
            assert manager.state.last_error["message"] == "ImportError"
            assert "when" in manager.state.last_error
    
    def test_clear_error(self):
        """Limpa erro do estado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.set_error("test.py", "Error")
            assert manager.state.last_error is not None
            
            manager.clear_error()
            assert manager.state.last_error is None
    
    def test_error_log_truncation(self):
        """Log de erro é truncado em 1000 chars."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            long_log = "x" * 2000
            manager.set_error("test.py", "Error", long_log)
            
            assert len(manager.state.last_error["log_excerpt"]) == 1000


class TestFileTracking:
    """Testes de rastreamento de arquivos."""
    
    def test_add_file_touched(self):
        """Adiciona arquivo modificado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.add_file_touched("src/main.py")
            
            assert "src/main.py" in manager.state.files_touched
    
    def test_add_duplicate_file(self):
        """Não adiciona arquivo duplicado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Teste")
            
            manager.add_file_touched("file.py")
            manager.add_file_touched("file.py")
            
            assert manager.state.files_touched.count("file.py") == 1
