"""Processamento de linguagem natural simples para detectar intenções."""

from typing import Optional, Tuple
from .models import AgentMode


class IntentDetector:
    """Detecta intenção e modo de agente baseado em entrada natural."""
    
    # Palavras-chave por modo de agente
    KEYWORDS = {
        AgentMode.ARCHITECT: [
            "arquitetura", "estrutura", "estruturar", "organizar", "planejar",
            "design", "padrão", "padrões", "modelar", "definir estrutura",
            "escolher", "dividir", "módulos", "componentes", "camadas"
        ],
        AgentMode.IMPLEMENTER: [
            "implementar", "criar", "adicionar", "desenvolver", "codificar",
            "escrever", "fazer", "construir", "gerar", "feature",
            "funcionalidade", "endpoint", "função", "classe", "método",
            "api", "rota", "controller", "service", "modelo"
        ],
        AgentMode.DEBUGGER: [
            "corrigir", "bug", "erro", "problema", "falha", "debugar",
            "investigar", "analisar erro", "exception", "stacktrace",
            "não funciona", "quebrado", "crash", "travando", "consertar"
        ],
        AgentMode.REVIEWER: [
            "revisar", "review", "verificar", "checar", "validar",
            "analisar código", "qualidade", "melhorar", "refatorar",
            "otimizar", "code review", "pr", "pull request", "diff"
        ],
        AgentMode.DOCUMENTER: [
            "documentar", "documentação", "readme", "docs", "explicar",
            "comentar", "comentários", "docstring", "exemplo",
            "tutorial", "guia", "manual", "ajuda", "how-to"
        ],
        AgentMode.OPS: [
            "deploy", "ci", "cd", "docker", "container", "kubernetes",
            "github actions", "pipeline", "build", "automatizar",
            "script", "infraestrutura", "devops", "automation"
        ]
    }
    
    @classmethod
    def detect_mode(cls, text: str) -> AgentMode:
        """Detecta o modo de agente mais apropriado para o texto.
        
        Args:
            text: Texto de entrada do usuário
            
        Returns:
            Modo de agente detectado (padrão: IMPLEMENTER)
        """
        text_lower = text.lower()
        
        # Contar matches por modo
        scores = {mode: 0 for mode in AgentMode}
        
        for mode, keywords in cls.KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[mode] += 1
        
        # Retornar modo com maior score
        max_score = max(scores.values())
        
        if max_score == 0:
            # Nenhuma palavra-chave encontrada, usar IMPLEMENTER como padrão
            return AgentMode.IMPLEMENTER
        
        # Retornar modo com maior score
        for mode, score in scores.items():
            if score == max_score:
                return mode
        
        return AgentMode.IMPLEMENTER
    
    @classmethod
    def extract_goal(cls, text: str) -> str:
        """Extrai objetivo limpo do texto.
        
        Remove palavras de ação redundantes e normaliza.
        
        Args:
            text: Texto de entrada
            
        Returns:
            Objetivo extraído e normalizado
        """
        # Remover palavras de ação comuns no início
        prefixes_to_remove = [
            "quero ", "preciso ", "gostaria de ", "pode ", "poderia ",
            "vou ", "vamos ", "me ajude a ", "ajude-me a "
        ]
        
        text_lower = text.lower()
        for prefix in prefixes_to_remove:
            if text_lower.startswith(prefix):
                text = text[len(prefix):]
                break
        
        # Capitalizar primeira letra
        return text[0].upper() + text[1:] if text else text
