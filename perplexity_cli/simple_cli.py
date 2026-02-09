"""CLI conversacional simples - estilo Claude Code.

Uso:
    perplexity-cli
    
    Você: criar uma API REST em Python
    Agente: [executa automaticamente]
    
    Você: adicionar testes
    Agente: [executa automaticamente]
"""

import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from .state import StateManager
from .nlp import IntentDetector
from .models import AgentMode
from .executor import ExecutionPipeline


class SimpleAgent:
    """Agente conversacional simples."""
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
        self.console = Console()
        self.state_manager = StateManager(str(self.workspace))
        self.intent_detector = IntentDetector()
        self.executor = ExecutionPipeline(self.state_manager, self.console)
        self.session_active = True
        
        # Inicializar estado se necessário
        if not self.state_manager.load():
            self.state_manager.create_initial_state(
                "Sessão interativa",
                AgentMode.IMPLEMENTER.value
            )
    
    def welcome(self):
        """Mensagem de boas-vindas."""
        self.console.print()
        self.console.print(Panel(
            "[bold cyan]Perplexity Agent CLI[/bold cyan]\n\n"
            "Digite o que você quer fazer e eu executo.\n"
            "Exemplos:\n"
            "  • criar uma API REST\n"
            "  • adicionar testes\n"
            "  • corrigir bug no arquivo X\n"
            "  • documentar o código\n\n"
            "[dim]Digite 'sair' para encerrar[/dim]",
            title="⚡ Bem-vindo",
            border_style="cyan"
        ))
        self.console.print(f"\n[dim]Workspace:[/dim] {self.workspace}\n")
    
    def process_input(self, user_input: str) -> bool:
        """Processa entrada do usuário.
        
        Returns:
            True se deve continuar, False para sair
        """
        user_input = user_input.strip()
        
        # Comandos de saída
        if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
            return False
        
        # Input vazio
        if not user_input:
            return True
        
        # Detectar intenção
        mode, goal = self.intent_detector.detect_intent_and_goal(user_input)
        
        # Atualizar modo se detectado diferente
        if mode != AgentMode[self.state_manager.state.agent_mode]:
            self.state_manager.state.agent_mode = mode.value
            self.state_manager.save()
        
        # Atualizar objetivo
        self.state_manager.state.goal = goal
        self.state_manager.save()
        
        # Exibir o que foi entendido
        self.console.print()
        self.console.print(f"[cyan]→ Modo:[/cyan] {mode.value}")
        self.console.print(f"[cyan]→ Objetivo:[/cyan] {goal}")
        self.console.print()
        
        # EXECUTAR AUTOMATICAMENTE
        self.execute_task(goal, mode)
        
        return True
    
    def execute_task(self, goal: str, mode: AgentMode):
        """Executa tarefa automaticamente.
        
        Args:
            goal: Objetivo a executar
            mode: Modo do agente
        """
        self.console.print("[yellow]⏳ Executando...[/yellow]\n")
        
        try:
            # Pipeline A-E simplificado
            
            # A: Critérios
            criteria = [f"Completar: {goal}", "Código funcional", "Testes passando"]
            
            # B: Inventário
            self.console.print("[dim]1. Analisando workspace...[/dim]")
            self.executor.inventory_repo()
            
            # C: Plano
            self.console.print("[dim]2. Criando plano...[/dim]")
            plan_items = self._generate_plan(goal, mode)
            self.executor.create_plan(plan_items)
            
            # D: Execução
            self.console.print("[dim]3. Executando etapas...[/dim]\n")
            for item in plan_items:
                self.executor.execute_step(
                    item['step'],
                    item['action'],
                    item.get('checkpoint')
                )
            
            # E: Fechamento
            files_modified = [item.get('file', 'unknown') for item in plan_items]
            next_steps = self._suggest_next_steps(goal, mode)
            
            self.console.print()
            self.console.print("[green bold]✓ Concluído![/green bold]\n")
            
            if next_steps:
                self.console.print("[bold]Próximos passos sugeridos:[/bold]")
                for i, step in enumerate(next_steps, 1):
                    self.console.print(f"  {i}. {step}")
            
        except Exception as e:
            self.console.print(f"[red]❌ Erro:[/red] {e}")
            self.console.print("\n[yellow]Tente reformular o pedido.[/yellow]")
    
    def _generate_plan(self, goal: str, mode: AgentMode) -> list:
        """Gera plano baseado no objetivo.
        
        Args:
            goal: Objetivo
            mode: Modo do agente
            
        Returns:
            Lista de etapas do plano
        """
        # Plano genérico - em produção seria gerado por LLM
        plan = [
            {
                'step': 1,
                'action': f"Preparar ambiente para: {goal}",
                'checkpoint': 'CP1:prepare',
                'file': 'setup'
            },
            {
                'step': 2,
                'action': f"Implementar: {goal}",
                'checkpoint': 'CP2:implement',
                'file': 'main'
            },
            {
                'step': 3,
                'action': "Validar e testar",
                'checkpoint': 'CP3:test',
                'file': 'tests'
            }
        ]
        
        return plan
    
    def _suggest_next_steps(self, goal: str, mode: AgentMode) -> list:
        """Sugere próximos passos.
        
        Args:
            goal: Objetivo completado
            mode: Modo usado
            
        Returns:
            Lista de sugestões
        """
        suggestions = {
            AgentMode.ARCHITECT: [
                "Implementar a arquitetura definida",
                "Revisar estrutura criada"
            ],
            AgentMode.IMPLEMENTER: [
                "Adicionar testes",
                "Revisar código implementado",
                "Documentar funcionalidades"
            ],
            AgentMode.DEBUGGER: [
                "Executar testes",
                "Revisar correções aplicadas"
            ],
            AgentMode.REVIEWER: [
                "Aplicar melhorias sugeridas",
                "Executar testes novamente"
            ],
            AgentMode.DOCUMENTER: [
                "Revisar documentação",
                "Adicionar exemplos"
            ],
            AgentMode.OPS: [
                "Testar pipeline",
                "Fazer deploy"
            ]
        }
        
        return suggestions.get(mode, ["Continuar desenvolvimento"])
    
    def run(self):
        """Loop principal do agente."""
        self.welcome()
        
        while self.session_active:
            try:
                # Prompt simples
                user_input = Prompt.ask(
                    "[bold cyan]Você[/bold cyan]",
                    default=""
                )
                
                # Processar
                should_continue = self.process_input(user_input)
                
                if not should_continue:
                    break
                
                self.console.print()  # Linha em branco
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Sessão interrompida.[/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]Erro:[/red] {e}")
        
        # Despedida
        self.console.print("\n[cyan]Até logo! 👋[/cyan]\n")


@click.command()
@click.option(
    '--workspace',
    default='.',
    help='Workspace directory',
    type=click.Path(exists=True)
)
def main(workspace: str):
    """Perplexity Agent CLI - Interface conversacional simples.
    
    Apenas fale o que quer fazer e o agente executa.
    """
    agent = SimpleAgent(workspace)
    agent.run()


if __name__ == '__main__':
    main()
