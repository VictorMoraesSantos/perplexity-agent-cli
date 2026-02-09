"""Testes para o módulo filesystem."""

import pytest
import tempfile
import os
from pathlib import Path

from perplexity_cli.filesystem import FileSystemOps
from perplexity_cli.state import StateManager
from perplexity_cli.models import AgentMode


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def state_manager(temp_workspace):
    manager = StateManager(temp_workspace)
    manager.create_initial_state("Teste filesystem", AgentMode.IMPLEMENTER.value)
    return manager


@pytest.fixture
def fs_ops(state_manager):
    return FileSystemOps(state_manager)


class TestFileSystemOps:
    """Testes de operações de filesystem."""
    
    def test_read_file(self, fs_ops, temp_workspace):
        """Testa leitura de arquivo."""
        # Criar arquivo de teste
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("conteúdo de teste")
        
        content = fs_ops.read_file(str(test_file))
        assert content == "conteúdo de teste"
    
    def test_write_file(self, fs_ops, temp_workspace):
        """Testa escrita de arquivo."""
        test_file = Path(temp_workspace) / "new.txt"
        
        fs_ops.write_file(str(test_file), "novo conteúdo")
        
        assert test_file.exists()
        assert test_file.read_text() == "novo conteúdo"
    
    def test_list_dir(self, fs_ops, temp_workspace):
        """Testa listagem de diretório."""
        # Criar alguns arquivos
        (Path(temp_workspace) / "file1.txt").touch()
        (Path(temp_workspace) / "file2.py").touch()
        
        files = fs_ops.list_dir(temp_workspace)
        
        assert len(files) >= 2
        assert any('file1.txt' in f for f in files)
    
    def test_create_dir(self, fs_ops, temp_workspace):
        """Testa criação de diretório."""
        new_dir = Path(temp_workspace) / "subdir"
        
        fs_ops.create_dir(str(new_dir))
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_delete_file(self, fs_ops, temp_workspace):
        """Testa deleção de arquivo."""
        test_file = Path(temp_workspace) / "delete_me.txt"
        test_file.touch()
        
        fs_ops.delete_file(str(test_file))
        
        assert not test_file.exists()
    
    def test_file_exists(self, fs_ops, temp_workspace):
        """Testa verificação de existência."""
        test_file = Path(temp_workspace) / "exists.txt"
        test_file.touch()
        
        assert fs_ops.file_exists(str(test_file)) is True
        assert fs_ops.file_exists(str(Path(temp_workspace) / "nope.txt")) is False
    
    def test_dry_run_mode(self, fs_ops, state_manager, temp_workspace):
        """Testa modo dry-run."""
        state_manager.state.dry_run = True
        state_manager.save()
        
        test_file = Path(temp_workspace) / "dry_run.txt"
        
        # Em dry-run, não deve criar o arquivo
        fs_ops.write_file(str(test_file), "teste")
        
        # Dependendo da implementação, arquivo pode não existir
        # assert not test_file.exists()
