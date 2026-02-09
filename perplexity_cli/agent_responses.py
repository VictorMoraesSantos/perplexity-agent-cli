"""Respostas conversacionais do Perplexity Agent."""

import random
from .models import AgentMode


class AgentResponses:
    """Gera respostas naturais do agente."""
    
    GREETINGS = [
        "Olá! Como posso ajudar você hoje?",
        "Oi! Estou pronto para trabalhar. O que você precisa?",
        "Olá! Pronto para começar. Qual é a tarefa?",
        "E aí! Vamos construir algo legal juntos?",
        "Olá! Diga o que precisa e eu cuido do resto."
    ]
    
    CONFIRMATIONS = {
        AgentMode.ARCHITECT: [
            "Perfeito! Vou estruturar isso para você.",
            "Entendi! Vou definir a arquitetura.",
            "Certo! Deixe-me planejar a estrutura ideal.",
            "Ok! Vou organizar tudo de forma escalváel."
        ],
        AgentMode.IMPLEMENTER: [
            "Entendi! Vou implementar isso agora.",
            "Perfeito! Deixe-me codificar isso para você.",
            "Certo! Vou criar isso rapidinho.",
            "Ok! Mãos à obra, vou fazer isso funcionar.",
            "Beleza! Vou desenvolver isso com capricho."
        ],
        AgentMode.DEBUGGER: [
            "Entendi! Vou investigar esse problema.",
            "Ok! Deixe-me analisar e corrigir isso.",
            "Certo! Vou debugar e resolver para você.",
            "Perfeito! Vou encontrar e consertar o bug."
        ],
        AgentMode.REVIEWER: [
            "Entendi! Vou revisar tudo com atenção.",
            "Certo! Deixe-me verificar a qualidade do código.",
            "Ok! Vou analisar e dar feedback construtivo.",
            "Perfeito! Vou garantir que tudo esteja nos conformes."
        ],
        AgentMode.DOCUMENTER: [
            "Entendi! Vou documentar isso detalhadamente.",
            "Certo! Deixe-me criar uma documentação clara.",
            "Ok! Vou explicar tudo de forma compreensível.",
            "Perfeito! Vou deixar bem documentado."
        ],
        AgentMode.OPS: [
            "Entendi! Vou configurar a infraestrutura.",
            "Certo! Deixe-me automatizar isso.",
            "Ok! Vou preparar o pipeline de deploy.",
            "Perfeito! Vou deixar tudo pronto para produção."
        ]
    }
    
    WORKING_MESSAGES = [
        "Deixe-me analisar o workspace e preparar tudo...",
        "Analisando o projeto e criando um plano...",
        "Preparando as ferramentas necessárias...",
        "Organizando as etapas para executar...",
        "Verificando o contexto e montando a estratégia..."
    ]
    
    COMPLETION_MESSAGES = [
        "Pronto! Tudo feito.",
        "Concluído! Ficou excelente.",
        "Terminado! Veja o resultado.",
        "Finalizado! Espero que goste.",
        "Feito! Próximo passo?"
    ]
    
    SUGGESTION_INTROS = [
        "Algumas sugestões do que fazer agora:",
        "Próximos passos recomendados:",
        "Você pode continuar com:",
        "Sugestões de continuidade:",
        "O que acha de:"
    ]
    
    @classmethod
    def greeting(cls) -> str:
        """Retorna saudação aleatória."""
        return random.choice(cls.GREETINGS)
    
    @classmethod
    def confirm_task(cls, mode: AgentMode, goal: str) -> str:
        """Confirma entendimento da tarefa.
        
        Args:
            mode: Modo do agente
            goal: Objetivo a executar
            
        Returns:
            Mensagem de confirmação
        """
        confirmations = cls.CONFIRMATIONS.get(mode, cls.CONFIRMATIONS[AgentMode.IMPLEMENTER])
        confirmation = random.choice(confirmations)
        return confirmation
    
    @classmethod
    def working_message(cls) -> str:
        """Retorna mensagem de trabalho em progresso."""
        return random.choice(cls.WORKING_MESSAGES)
    
    @classmethod
    def completion_message(cls) -> str:
        """Retorna mensagem de conclusão."""
        return random.choice(cls.COMPLETION_MESSAGES)
    
    @classmethod
    def suggestion_intro(cls) -> str:
        """Retorna introdução para sugestões."""
        return random.choice(cls.SUGGESTION_INTROS)
    
    @classmethod
    def is_greeting(cls, text: str) -> bool:
        """Verifica se o texto é uma saudação.
        
        Args:
            text: Texto do usuário
            
        Returns:
            True se for saudação
        """
        greetings = [
            "oi", "olá", "ola", "hey", "opa", "e ai", "e aí",
            "bom dia", "boa tarde", "boa noite", "hello", "hi",
            "olá agente", "oi agente", "hey agente"
        ]
        text_lower = text.lower().strip()
        return any(greeting in text_lower for greeting in greetings)
    
    @classmethod
    def is_thanks(cls, text: str) -> bool:
        """Verifica se o texto é agradecimento.
        
        Args:
            text: Texto do usuário
            
        Returns:
            True se for agradecimento
        """
        thanks = [
            "obrigado", "obrigada", "valeu", "vlw", "thanks",
            "thank you", "graças", "brigadao", "brigado"
        ]
        text_lower = text.lower().strip()
        return any(thank in text_lower for thank in thanks)
    
    @classmethod
    def thanks_response(cls) -> str:
        """Resposta para agradecimento."""
        responses = [
            "Por nada! Estou aqui para ajudar.",
            "Disponível! É um prazer ajudar.",
            "Sempre! Pode contar comigo.",
            "De nada! Foi um prazer trabalhar nisso.",
            "👍 Qualquer coisa, é só chamar!"
        ]
        return random.choice(responses)
