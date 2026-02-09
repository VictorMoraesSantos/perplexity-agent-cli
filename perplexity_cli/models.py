"""Modelos e tipos do sistema."""

from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass


class AgentMode(str, Enum):
    """Modos de operação do agente."""
    ARCHITECT = "ARCHITECT"
    IMPLEMENTER = "IMPLEMENTER"
    DEBUGGER = "DEBUGGER"
    REVIEWER = "REVIEWER"
    DOCUMENTER = "DOCUMENTER"
    OPS = "OPS"


@dataclass
class AgentProfile:
    """Perfil de comportamento de um agente."""
    mode: AgentMode
    description: str
    focus: List[str]
    typical_actions: List[str]
    

# Definição dos perfis de agente
AGENT_PROFILES: Dict[AgentMode, AgentProfile] = {
    AgentMode.ARCHITECT: AgentProfile(
        mode=AgentMode.ARCHITECT,
        description="Define arquitetura, divide tarefas, escolhe padrões e estrutura",
        focus=[
            "Estrutura de pastas",
            "Padrões de design",
            "Divisão de responsabilidades",
            "Definição de interfaces"
        ],
        typical_actions=[
            "Criar estrutura de diretórios",
            "Definir módulos e pacotes",
            "Especificar contratos de API",
            "Escolher bibliotecas e frameworks"
        ]
    ),
    AgentMode.IMPLEMENTER: AgentProfile(
        mode=AgentMode.IMPLEMENTER,
        description="Implementa código e alterações em arquivos",
        focus=[
            "Escrita de código",
            "Implementação de features",
            "Refatoração",
            "Otimização"
        ],
        typical_actions=[
            "Criar/modificar arquivos",
            "Implementar funções",
            "Adicionar testes",
            "Corrigir bugs simples"
        ]
    ),
    AgentMode.DEBUGGER: AgentProfile(
        mode=AgentMode.DEBUGGER,
        description="Investiga erros, reproduz, cria hipóteses e corrige",
        focus=[
            "Análise de stacktraces",
            "Reprodução de bugs",
            "Diagnóstico sistemático",
            "Correções mínimas"
        ],
        typical_actions=[
            "Analisar logs de erro",
            "Criar casos de teste",
            "Propor hipóteses",
            "Aplicar correções cirúrgicas"
        ]
    ),
    AgentMode.REVIEWER: AgentProfile(
        mode=AgentMode.REVIEWER,
        description="Revisa diffs, qualidade, consistência e segurança",
        focus=[
            "Qualidade de código",
            "Padrões e convenções",
            "Edge cases",
            "Segurança"
        ],
        typical_actions=[
            "Revisar diffs",
            "Verificar testes",
            "Identificar problemas de segurança",
            "Sugerir melhorias"
        ]
    ),
    AgentMode.DOCUMENTER: AgentProfile(
        mode=AgentMode.DOCUMENTER,
        description="Atualiza README, docs, comentários e exemplos",
        focus=[
            "Documentação técnica",
            "Exemplos de uso",
            "Comentários de código",
            "Guias e tutoriais"
        ],
        typical_actions=[
            "Escrever/atualizar README",
            "Criar exemplos",
            "Documentar APIs",
            "Adicionar docstrings"
        ]
    ),
    AgentMode.OPS: AgentProfile(
        mode=AgentMode.OPS,
        description="Scripts, CI, Docker, automações e packaging",
        focus=[
            "CI/CD",
            "Containerização",
            "Automação",
            "Deploy e distribuição"
        ],
        typical_actions=[
            "Configurar GitHub Actions",
            "Criar Dockerfiles",
            "Scripts de build",
            "Setup de hooks git"
        ]
    )
}
