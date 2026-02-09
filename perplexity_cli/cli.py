"""Interface de linha de comando do Perplexity Agent CLI."""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .state import StateManager
from .commands import CommandHandler
from .models import AgentMode
from .nlp import IntentDetector
from .executor import ExecutionPipeline
from .agent_responses import AgentResponses


class PerplexityCLI:
    def __init__(self, workspace: str, goal: Optional[str] = None, mode: Optional[str] = None, auto_mode: bool = True):
        self.workspace = Path(workspace).resolve()
        self.console = Console()
        self.state_manager = StateManager(str(self.workspace))
        self.command_handler = CommandHandler(self.state_manager, self.console)
        self.intent_detector = IntentDetector()
        self.executor = ExecutionPipeline(self.state_manager, self.console)
        self.responses = AgentResponses()
        self.auto_mode = auto_mode
        self.session_active = True
        
        # Inicializar estado
        if not self.state_manager.load():
            initial_goal = goal or "Sessão interativa"
            initial_mode = mode or AgentMode.IMPLEMENTER.value
            self.state_manager.create_initial_state(initial_goal, initial_mode)
        elif goal:
            self.state_manager.state.goal = goal
            self.state_manager.save()
    
    def welcome(self):
        """Mensagem de boas-vindas."""
        mode_label = "[cyan]AUTO[/cyan]" if self.auto_mode else "MANUAL"
        
        self.console.print()
        self.console.print(Panel(
            f"[bold cyan]Perplexity Agent CLI[/bold cyan]\n\n"
            f"Modo: {mode_label}\n"
            f"Workspace: {self.workspace}\n\n"
            f"[dim]Digite comandos naturais ou /help para ajuda[/dim]",
            title="⚡ Sessão Iniciada",
            border_style="cyan"
        ))
        self.console.print()
    
    def process_input(self, user_input: str) -> bool:
        """Processa entrada do usuário.
        
        Returns:
            True se deve continuar, False para sair
        """
        user_input = user_input.strip()
        
        # Input vazio
        if not user_input:
            return True
        
        # Comandos de saída
        if user_input.lower() in ['exit', 'quit', 'sair', 'q']:
            return False
        
        # Comandos com /
        if user_input.startswith('/'):
            return self.handle_command(user_input)
        
        # Linguagem natural
        return self.handle_natural_input(user_input)
    
    def handle_command(self, command: str) -> bool:
        """Trata comandos que começam com /.
        
        Args:
            command: Comando com /
            
        Returns:
            True para continuar
        """
        parts = command[1:].split(maxsplit=1)
        cmd_name = parts[0].lower()
        cmd_arg = parts[1] if len(parts) > 1 else ""
        
        if cmd_name == 'help':
            self.command_handler.cmd_help(cmd_arg)
        elif cmd_name == 'status':
            self.command_handler.cmd_status(cmd_arg)
        elif cmd_name == 'plan':
            self.command_handler.cmd_plan(cmd_arg)
        elif cmd_name == 'agent':
            self.command_handler.cmd_agent(cmd_arg)
        elif cmd_name == 'workspace':
            self.command_handler.cmd_workspace(cmd_arg)
        elif cmd_name == 'dry-run':
            self.command_handler.cmd_dry_run(cmd_arg)
        elif cmd_name == 'watch':
            self.command_handler.cmd_watch(cmd_arg)
        elif cmd_name == 'auto':
            if cmd_arg.lower() == 'on':
                self.auto_mode = True
                self.console.print("[green]✓ Modo AUTO ativado[/green]")
            elif cmd_arg.lower() == 'off':
                self.auto_mode = False
                self.console.print("[yellow]✓ Modo AUTO desativado[/yellow]")
        else:
            self.console.print(f"[red]Comando desconhecido:[/red] /{cmd_name}")
            self.console.print("[dim]Use /help para ver comandos disponíveis[/dim]")
        
        return True
    
    def handle_natural_input(self, user_input: str) -> bool:
        """Trata entrada em linguagem natural.
        
        Args:
            user_input: Texto do usuário
            
        Returns:
            True para continuar
        """
        self.console.print()
        
        # Verificar saudações
        if self.responses.is_greeting(user_input):
            self.console.print(f"[bold cyan]🤖 Perplexity:[/bold cyan] {self.responses.greeting()}")
            self.console.print()
            return True
        
        # Verificar agradecimentos
        if self.responses.is_thanks(user_input):
            self.console.print(f"[bold cyan]🤖 Perplexity:[/bold cyan] {self.responses.thanks_response()}")
            self.console.print()
            return True
        
        # Detectar intenção
        mode, goal = self.intent_detector.detect_intent_and_goal(user_input)
        
        # Atualizar modo se necessário
        current_mode = self.state_manager.state.agent_mode
        if mode.value != current_mode:
            self.state_manager.state.agent_mode = mode.value
            self.state_manager.save()
        
        # Atualizar objetivo
        self.state_manager.state.goal = goal
        self.state_manager.save()
        
        # 🤖 RESPOSTA DO AGENTE
        confirmation = self.responses.confirm_task(mode, goal)
        self.console.print(f"[bold cyan]🤖 Perplexity:[/bold cyan] {confirmation}")
        
        if self.auto_mode:
            working_msg = self.responses.working_message()
            self.console.print(f"[dim]{working_msg}[/dim]")
        
        self.console.print()
        
        # Exibir detecção
        self.console.print(f"[cyan]→ Modo:[/cyan] {mode.value}")
        self.console.print(f"[cyan]→ Objetivo:[/cyan] {goal}")
        self.console.print()
        
        # 🚀 EXECUTAR AUTOMATICAMENTE SE AUTO_MODE
        if self.auto_mode:
            self.execute_automatically(goal, mode)
        else:
            # Modo manual - apenas informa
            self.console.print("[dim]Use /plan para ver o plano, /status para estado[/dim]")
        
        return True
    
    def execute_automatically(self, goal: str, mode: AgentMode):
        """Executa tarefa automaticamente.
        
        Args:
            goal: Objetivo a executar
            mode: Modo do agente
        """
        self.console.print("[yellow]⏳ Executando...[/yellow]\n")
        
        try:
            # Gerar plano
            plan_items = self._generate_plan(goal, mode)
            
            # Executar pipeline
            self.console.print("[dim]1. Analisando workspace...[/dim]")
            self.executor.inventory_repo()
            
            self.console.print("[dim]2. Criando plano...[/dim]")
            self.executor.create_plan(plan_items)
            
            self.console.print("[dim]3. Executando etapas...[/dim]\n")
            for item in plan_items:
                success = self.executor.execute_step(
                    item['step'],
                    item['action'],
                    item.get('checkpoint')
                )
                if not success:
                    self.console.print("[yellow]⚠ Etapa falhou, continuando...[/yellow]")
            
            # Concluir
            next_steps = self._suggest_next_steps(mode)
            
            # 🤖 MENSAGEM DE CONCLUSÃO
            self.console.print()
            completion = self.responses.completion_message()
            self.console.print(f"[bold green]✓ {completion}[/bold green]\n")
            
            if next_steps:
                suggestion_intro = self.responses.suggestion_intro()
                self.console.print(f"[bold cyan]🤖 Perplexity:[/bold cyan] {suggestion_intro}")
                for i, step in enumerate(next_steps, 1):
                    self.console.print(f"  {i}. {step}")
            
            self.console.print()
            
        except Exception as e:
            self.console.print(f"[red]❌ Erro na execução:[/red] {e}")
            self.console.print("[bold cyan]🤖 Perplexity:[/bold cyan] Tente um comando mais específico.\n")
    
    def _generate_plan(self, goal: str, mode: AgentMode) -> list:
        """Gera plano baseado no objetivo."""
        plan = [
            {
                'step': 1,
                'action': f"Preparar: {goal}",
                'checkpoint': 'CP1:prepare',
                'file': 'preparation'
            },
            {
                'step': 2,
                'action': f"Executar: {goal}",
                'checkpoint': 'CP2:execute',
                'file': 'implementation'
            },
            {
                'step': 3,
                'action': "Validar resultado",
                'checkpoint': 'CP3:validate',
                'file': 'validation'
            }
        ]
        return plan
    
    def _suggest_next_steps(self, mode: AgentMode) -> list:
        """Sugere próximos passos."""
        suggestions = {
            AgentMode.ARCHITECT: ["Implementar arquitetura", "Revisar estrutura"],
            AgentMode.IMPLEMENTER: ["Adicionar testes", "Documentar código"],
            AgentMode.DEBUGGER: ["Executar testes", "Verificar correções"],
            AgentMode.REVIEWER: ["Aplicar melhorias", "Validar qualidade"],
            AgentMode.DOCUMENTER: ["Revisar docs", "Adicionar exemplos"],
            AgentMode.OPS: ["Testar pipeline", "Fazer deploy"]
        }
        return suggestions.get(mode, ["Continuar desenvolvimento"])
    
    def run(self):
        """Loop principal."""
        self.welcome()
        
        prompt_label = "[cyan]AUTO[/cyan]" if self.auto_mode else "MANUAL"
        
        while self.session_active:
            try:
                user_input = Prompt.ask(f"[{prompt_label}] >", default="")
                
                should_continue = self.process_input(user_input)
                
                if not should_continue:
                    break
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Sessão encerrada.[/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]Erro:[/red] {e}")
                import traceback
                traceback.print_exc()
        
        self.console.print("\n[bold cyan]🤖 Perplexity:[/bold cyan] Até logo! 👋\n")


@click.command()
@click.option('--workspace', default='.', help='Diretório de trabalho')
@click.option('--goal', default=None, help='Objetivo inicial')
@click.option('--mode', default=None, help='Modo do agente')
@click.option('--no-auto', is_flag=True, help='Desabilitar modo AUTO')
@click.version_option(version='0.2.0')
def main(workspace: str, goal: Optional[str], mode: Optional[str], no_auto: bool):
    """Perplexity Agent CLI - Agente de engenharia de software."""
    try:
        cli = PerplexityCLI(
            workspace=workspace,
            goal=goal,
            mode=mode,
            auto_mode=not no_auto
        )
        cli.run()
    except Exception as e:
        console = Console()
        console.print(f"[red]Erro fatal:[/red] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
