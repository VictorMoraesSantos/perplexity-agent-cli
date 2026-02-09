"""Testes completos do módulo NLP."""

import pytest
from perplexity_cli.nlp import IntentDetector
from perplexity_cli.models import AgentMode


class TestIntentDetection:
    """Testes de detecção de intenção."""
    
    # TC-NLP-001: Detectar IMPLEMENTER
    @pytest.mark.parametrize("text,expected", [
        ("criar uma API REST", AgentMode.IMPLEMENTER),
        ("implementar autenticação", AgentMode.IMPLEMENTER),
        ("adicionar feature de login", AgentMode.IMPLEMENTER),
        ("desenvolver endpoint", AgentMode.IMPLEMENTER),
        ("escrever código para", AgentMode.IMPLEMENTER),
        ("construir uma função", AgentMode.IMPLEMENTER),
        ("fazer um serviço", AgentMode.IMPLEMENTER),
        ("codificar o módulo", AgentMode.IMPLEMENTER),
    ])
    def test_detect_implementer(self, text, expected):
        """TC-NLP-001: Detecta modo IMPLEMENTER."""
        result = IntentDetector.detect_mode(text)
        assert result == expected, f"Esperado {expected}, obtido {result} para '{text}'"
    
    # TC-NLP-002: Detectar DEBUGGER
    @pytest.mark.parametrize("text,expected", [
        ("corrigir bug no auth.py", AgentMode.DEBUGGER),
        ("debugar problema", AgentMode.DEBUGGER),
        ("erro no sistema", AgentMode.DEBUGGER),
        ("falha na API", AgentMode.DEBUGGER),
        ("investigar crash", AgentMode.DEBUGGER),
        ("analisar exception", AgentMode.DEBUGGER),
        ("consertar quebrado", AgentMode.DEBUGGER),
        ("não funciona", AgentMode.DEBUGGER),
    ])
    def test_detect_debugger(self, text, expected):
        """TC-NLP-002: Detecta modo DEBUGGER."""
        result = IntentDetector.detect_mode(text)
        assert result == expected, f"Esperado {expected}, obtido {result} para '{text}'"
    
    # TC-NLP-003: Detectar REVIEWER
    @pytest.mark.parametrize("text,expected", [
        ("revisar o código", AgentMode.REVIEWER),
        ("code review", AgentMode.REVIEWER),
        ("verificar qualidade", AgentMode.REVIEWER),
        ("checar PR", AgentMode.REVIEWER),
        ("analisar código", AgentMode.REVIEWER),
        ("validar implementação", AgentMode.REVIEWER),
        ("melhorar código", AgentMode.REVIEWER),
        ("refatorar função", AgentMode.REVIEWER),
    ])
    def test_detect_reviewer(self, text, expected):
        """TC-NLP-003: Detecta modo REVIEWER."""
        result = IntentDetector.detect_mode(text)
        assert result == expected, f"Esperado {expected}, obtido {result} para '{text}'"
    
    # TC-NLP-004: Detectar ARCHITECT
    @pytest.mark.parametrize("text,expected", [
        ("definir estrutura do projeto", AgentMode.ARCHITECT),
        ("planejar arquitetura", AgentMode.ARCHITECT),
        ("organizar módulos", AgentMode.ARCHITECT),
        ("escolher padrão de design", AgentMode.ARCHITECT),
        ("estruturar componentes", AgentMode.ARCHITECT),
        ("dividir responsabilidades", AgentMode.ARCHITECT),
        ("modelar sistema", AgentMode.ARCHITECT),
    ])
    def test_detect_architect(self, text, expected):
        """TC-NLP-004: Detecta modo ARCHITECT."""
        result = IntentDetector.detect_mode(text)
        assert result == expected, f"Esperado {expected}, obtido {result} para '{text}'"
    
    # TC-NLP-005: Detectar DOCUMENTER
    @pytest.mark.parametrize("text,expected", [
        ("documentar a API", AgentMode.DOCUMENTER),
        ("escrever README", AgentMode.DOCUMENTER),
        ("criar docs", AgentMode.DOCUMENTER),
        ("adicionar comentários", AgentMode.DOCUMENTER),
        ("explicar função", AgentMode.DOCUMENTER),
        ("gerar documentação", AgentMode.DOCUMENTER),
        ("criar tutorial", AgentMode.DOCUMENTER),
        ("fazer guia", AgentMode.DOCUMENTER),
    ])
    def test_detect_documenter(self, text, expected):
        """TC-NLP-005: Detecta modo DOCUMENTER."""
        result = IntentDetector.detect_mode(text)
        assert result == expected, f"Esperado {expected}, obtido {result} para '{text}'"
    
    # TC-NLP-006: Detectar OPS
    @pytest.mark.parametrize("text,expected", [
        ("configurar CI/CD", AgentMode.OPS),
        ("setup GitHub Actions", AgentMode.OPS),
        ("criar Dockerfile", AgentMode.OPS),
        ("deploy da aplicação", AgentMode.OPS),
        ("automatizar build", AgentMode.OPS),
        ("pipeline de CI", AgentMode.OPS),
        ("kubernetes config", AgentMode.OPS),
        ("script de deploy", AgentMode.OPS),
    ])
    def test_detect_ops(self, text, expected):
        """TC-NLP-006: Detecta modo OPS."""
        result = IntentDetector.detect_mode(text)
        assert result == expected, f"Esperado {expected}, obtido {result} para '{text}'"
    
    # TC-NLP-007: Entrada Ambígua
    def test_ambiguous_input_defaults_to_implementer(self):
        """TC-NLP-007: Entrada ambígua usa IMPLEMENTER como padrão."""
        result = IntentDetector.detect_mode("fazer algo")
        assert result == AgentMode.IMPLEMENTER
    
    # TC-NLP-008: Extração de Goal
    @pytest.mark.parametrize("input_text,expected_goal", [
        ("quero criar uma API", "Criar uma API"),
        ("preciso adicionar testes", "Adicionar testes"),
        ("gostaria de implementar login", "Implementar login"),
        ("pode criar documentação", "Criar documentação"),
        ("ajude-me a corrigir bug", "Corrigir bug"),
        ("criar uma API", "Criar uma API"),  # Sem prefixo
    ])
    def test_extract_goal(self, input_text, expected_goal):
        """TC-NLP-008: Extração de objetivo."""
        result = IntentDetector.extract_goal(input_text)
        assert result == expected_goal, f"Esperado '{expected_goal}', obtido '{result}'"
    
    # TC-NLP-009: Unicode e Acentos
    def test_unicode_handling(self):
        """TC-NLP-009: Trata corretamente unicode e acentos."""
        text = "criação de módulo de autenticação com ç e ã"
        result = IntentDetector.detect_mode(text)
        # Deve detectar IMPLEMENTER
        assert result == AgentMode.IMPLEMENTER
    
    # Teste adicional: emojis
    def test_emoji_handling(self):
        """Testa tratamento de emojis no texto."""
        text = "criar uma API 🚀 com autentição 🔐"
        result = IntentDetector.detect_mode(text)
        assert result == AgentMode.IMPLEMENTER
    
    # Teste adicional: texto vazio
    def test_empty_text(self):
        """Testa entrada vazia."""
        result = IntentDetector.detect_mode("")
        assert result == AgentMode.IMPLEMENTER  # Padrão
    
    # Teste adicional: apenas espaços
    def test_whitespace_only(self):
        """Testa entrada apenas com espaços."""
        result = IntentDetector.detect_mode("     ")
        assert result == AgentMode.IMPLEMENTER  # Padrão
