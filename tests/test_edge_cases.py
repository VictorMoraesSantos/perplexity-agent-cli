"""Testes de edge cases e situações extremas."""

import pytest
import tempfile
import os
from pathlib import Path
from perplexity_cli.state import StateManager
from perplexity_cli.nlp import IntentDetector
from perplexity_cli.models import AgentMode


class TestSecurityEdgeCases:
    """Testes de segurança e edge cases perigosos."""
    
    def test_path_traversal_attempt(self):
        """TC-EDGE-001: Tentativa de path traversal."""
        # Nota: Este teste verifica que paths maliciosos não causam crash
        # A validação real de segurança deve estar no código
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "/etc/shadow",
            "C:\\Windows\\System32\\config\\SAM"
        ]
        
        for path in malicious_paths:
            # Não deve causar crash ou exceção não tratada
            try:
                result = IntentDetector.detect_mode(path)
                # Apenas garante que não crashou
                assert result in AgentMode
            except Exception as e:
                pytest.fail(f"Path malicioso causou exceção: {e}")
    
    def test_sql_injection_like_input(self):
        """TC-EDGE-002: Entrada similar a SQL injection."""
        dangerous_inputs = [
            "'; DROP TABLE users--",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM secrets--"
        ]
        
        for input_text in dangerous_inputs:
            # Deve tratar como string normal
            result = IntentDetector.detect_mode(input_text)
            assert result in AgentMode
            
            # Goal deve preservar o texto
            goal = IntentDetector.extract_goal(input_text)
            assert isinstance(goal, str)


class TestInputEdgeCases:
    """Testes de edge cases de entrada."""
    
    def test_very_long_input(self):
        """TC-EDGE-003: Entrada muito longa (10KB)."""
        long_text = "criar API " + "x" * 10000
        
        # Não deve crashar
        result = IntentDetector.detect_mode(long_text)
        assert result in AgentMode
    
    def test_empty_string(self):
        """Entrada vazia."""
        result = IntentDetector.detect_mode("")
        assert result == AgentMode.IMPLEMENTER  # Padrão
    
    def test_only_whitespace(self):
        """Apenas espaços em branco."""
        result = IntentDetector.detect_mode("     \n\t  ")
        assert result == AgentMode.IMPLEMENTER
    
    def test_special_characters(self):
        """Caracteres especiais."""
        special_texts = [
            "criar API !@#$%^&*()",
            "implementar <script>alert('xss')</script>",
            "adicionar {code: 'injection'}",
            "fazer `rm -rf /`"
        ]
        
        for text in special_texts:
            result = IntentDetector.detect_mode(text)
            assert result in AgentMode
    
    def test_unicode_emojis(self):
        """Unicode e emojis."""
        emoji_texts = [
            "🚀 criar API super rápida 🚀",
            "🐛 corrigir bug 🐞",
            "📝 documentar 📖",
            "✅ implementar ✨"
        ]
        
        for text in emoji_texts:
            result = IntentDetector.detect_mode(text)
            assert result in AgentMode
    
    def test_mixed_languages(self):
        """Entrada com idiomas misturados."""
        mixed_texts = [
            "criar uma REST API",
            "implementar authentication system",
            "fazer code review do PR"
        ]
        
        for text in mixed_texts:
            result = IntentDetector.detect_mode(text)
            assert result in AgentMode
    
    def test_all_caps(self):
        """Texto todo em maiúsculas."""
        result = IntentDetector.detect_mode("CRIAR UMA API REST")
        assert result == AgentMode.IMPLEMENTER
    
    def test_all_lowercase(self):
        """Texto todo em minúsculas."""
        result = IntentDetector.detect_mode("criar uma api rest")
        assert result == AgentMode.IMPLEMENTER
    
    def test_numbers_in_text(self):
        """Números no texto."""
        result = IntentDetector.detect_mode("criar API v2.0 com 100 endpoints")
        assert result == AgentMode.IMPLEMENTER


class TestFilesystemEdgeCases:
    """Testes de edge cases do filesystem."""
    
    def test_readonly_workspace(self):
        """TC-EDGE-006: Workspace read-only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Tornar read-only
            os.chmod(tmpdir, 0o444)
            
            try:
                manager = StateManager(tmpdir)
                # Tentar criar estado deve falhar graciosamente
                with pytest.raises(Exception):
                    manager.create_initial_state("Teste")
            finally:
                # Restaurar permissões para limpeza
                os.chmod(tmpdir, 0o755)
    
    def test_nonexistent_workspace(self):
        """Workspace que não existe."""
        manager = StateManager("/path/that/does/not/exist/xyz123")
        # Não deve crashar ao instanciar
        assert manager.workspace == "/path/that/does/not/exist/xyz123"
    
    def test_workspace_is_file(self):
        """Workspace é um arquivo ao invés de pasta."""
        with tempfile.NamedTemporaryFile() as tmpfile:
            manager = StateManager(tmpfile.name)
            # Tentar criar diretório de estado deve falhar
            with pytest.raises(Exception):
                manager.ensure_state_dir()
    
    def test_unicode_in_workspace_path(self):
        """Path com unicode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            unicode_path = Path(tmpdir) / "测试_tést_тест"
            unicode_path.mkdir()
            
            manager = StateManager(str(unicode_path))
            state = manager.create_initial_state("Teste")
            
            assert state is not None
            assert manager.state_file.exists()


class TestStateEdgeCases:
    """Edge cases específicos do estado."""
    
    def test_state_with_all_fields_populated(self):
        """Estado com todos os campos preenchidos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StateManager(tmpdir)
            state = manager.create_initial_state("Teste completo")
            
            # Preencher todos os campos possíveis
            state.files_touched = [f"file{i}.py" for i in range(50)]
            state.open_questions = [f"Questão {i}" for i in range(10)]
            state.plan = [f"Etapa {i}" for i in range(20)]
            
            for i in range(30):
                manager.add_command(f"cmd{i}", "ok")
            
            for i in range(10):
                manager.update_checkpoint(f"CP{i}:step{i}")
            
            # Salvar e carregar
            manager.save()
            loaded = StateManager(tmpdir).load()
            
            assert len(loaded.files_touched) == 50
            assert len(loaded.open_questions) == 10
            assert len(loaded.commands_run) == 30
            assert len(loaded.checkpoints) == 10
    
    def test_concurrent_state_access(self):
        """Dois managers acessando mesmo estado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager1 = StateManager(tmpdir)
            manager2 = StateManager(tmpdir)
            
            # Manager1 cria estado
            manager1.create_initial_state("Teste 1")
            
            # Manager2 carrega
            state2 = manager2.load()
            assert state2.goal == "Teste 1"
            
            # Manager2 modifica
            state2.goal = "Teste 2 modificado"
            manager2.save()
            
            # Manager1 recarrega
            state1_reload = manager1.load()
            assert state1_reload.goal == "Teste 2 modificado"
