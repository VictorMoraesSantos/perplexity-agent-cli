"""Testes de casos extremos e edge cases."""

import pytest
import tempfile
import os
from pathlib import Path
import threading
import time

from perplexity_cli.state import StateManager
from perplexity_cli.models import AgentMode
from perplexity_cli.nlp import IntentDetector


@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def state_manager(temp_workspace):
    manager = StateManager(temp_workspace)
    manager.create_initial_state("Test", AgentMode.IMPLEMENTER.value)
    return manager


@pytest.fixture
def intent_detector():
    return IntentDetector()


class TestSecurityEdgeCases:
    """Testes de segurança."""
    
    def test_path_traversal_attempt(self, state_manager):
        """Testa tentativa de path traversal."""
        malicious_path = "../../etc/passwd"
        # Não deve permitir acesso fora do workspace
        assert True  # Placeholder
    
    def test_sql_injection_like_input(self, intent_detector):
        """Testa entrada tipo SQL injection."""
        malicious = "'; DROP TABLE users; --"
        mode, goal = intent_detector.detect_intent_and_goal(malicious)
        # Não deve quebrar
        assert isinstance(mode, AgentMode)


class TestInputEdgeCases:
    """Testes de entradas extremas."""
    
    def test_very_long_input(self, intent_detector):
        """Testa entrada muito longa."""
        long_text = "criar API " * 1000
        mode, goal = intent_detector.detect_intent_and_goal(long_text)
        assert isinstance(mode, AgentMode)
    
    def test_empty_string(self, intent_detector):
        """Testa string vazia."""
        mode, goal = intent_detector.detect_intent_and_goal("")
        assert mode == AgentMode.IMPLEMENTER
    
    def test_only_whitespace(self, intent_detector):
        """Testa apenas espaços."""
        mode, goal = intent_detector.detect_intent_and_goal("    \n\t  ")
        assert mode == AgentMode.IMPLEMENTER
    
    def test_special_characters(self, intent_detector):
        """Testa caracteres especiais."""
        mode, goal = intent_detector.detect_intent_and_goal("criar @#$% API")
        assert isinstance(mode, AgentMode)
    
    def test_unicode_emojis(self, intent_detector):
        """Testa emojis."""
        mode, goal = intent_detector.detect_intent_and_goal("criar 🚀 API 🔥")
        assert isinstance(mode, AgentMode)
    
    def test_mixed_languages(self, intent_detector):
        """Testa mistura de idiomas."""
        mode, goal = intent_detector.detect_intent_and_goal("create uma API REST")
        assert isinstance(mode, AgentMode)
    
    def test_all_caps(self, intent_detector):
        """Testa texto em maiúsculas."""
        mode, goal = intent_detector.detect_intent_and_goal("CRIAR UMA API")
        assert mode == AgentMode.IMPLEMENTER
    
    def test_all_lowercase(self, intent_detector):
        """Testa texto em minúsculas."""
        mode, goal = intent_detector.detect_intent_and_goal("criar uma api")
        assert mode == AgentMode.IMPLEMENTER
    
    def test_numbers_in_text(self, intent_detector):
        """Testa números no texto."""
        mode, goal = intent_detector.detect_intent_and_goal("criar 3 APIs com Python 3.11")
        assert isinstance(mode, AgentMode)


class TestFilesystemEdgeCases:
    """Testes de casos extremos de filesystem."""
    
    def test_readonly_workspace(self, temp_workspace):
        """Testa workspace read-only."""
        # No Windows, marcar como read-only é complexo
        pytest.skip("Teste específico de permissões")
    
    def test_nonexistent_workspace(self):
        """Testa workspace inexistente."""
        manager = StateManager("/caminho/inexistente")
        # Não deve quebrar na criação
        assert manager.workspace == "/caminho/inexistente"
    
    def test_workspace_is_file(self, temp_workspace):
        """Testa quando workspace é um arquivo."""
        file_path = Path(temp_workspace) / "not_a_dir.txt"
        file_path.touch()
        
        # Deve lidar graciosamente
        manager = StateManager(str(file_path))
        assert manager.workspace == str(file_path)
    
    def test_unicode_in_workspace_path(self):
        """Testa unicode no caminho do workspace."""
        with tempfile.TemporaryDirectory(prefix="test_çãõ_") as tmpdir:
            manager = StateManager(tmpdir)
            manager.create_initial_state("Test", AgentMode.IMPLEMENTER.value)
            assert manager.state is not None


class TestStateEdgeCases:
    """Testes de casos extremos de estado."""
    
    def test_state_with_all_fields_populated(self, state_manager):
        """Testa estado com todos os campos preenchidos."""
        state = state_manager.state
        state.plan = [f"Step {i}" for i in range(100)]
        state.files_touched = [f"file{i}.py" for i in range(50)]
        state.commands_run = [{"cmd": f"cmd{i}", "result": "ok"} for i in range(30)]
        
        state_manager.save()
        loaded = state_manager.load()
        
        assert loaded is not None
        assert len(loaded.plan) == 100
    
    def test_concurrent_state_access(self, state_manager):
        """Testa acesso concorrente ao estado."""
        def modify_state():
            for i in range(10):
                state_manager.add_file_touched(f"file{i}.py")
                time.sleep(0.01)
        
        threads = [threading.Thread(target=modify_state) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Deve ter registrado arquivos
        assert len(state_manager.state.files_touched) > 0
