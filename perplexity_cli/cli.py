#!/usr/bin/env python3
"""Perplexity Agent CLI - Interface principal."""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from .state import StateManager, RunState
from .models import AgentMode, AGENT_PROFILES
from .commands import CommandHandler
from .utils import print_state, print_plan, print_welcome


console = Console()


class PerplexityCLI:
    """Classe principal do CLI."""
    
    def __init__(self, workspace: Optional[str] = None):
        self.workspace = workspace or os.getcwd()
        self.state_manager = StateManager(self.workspace)
        self.command_handler = CommandHandler(self.state_manager, console)
        self.running = True
        
    def start(self) -> None:
        """Inicia o CLI em modo interativo."""
        print_welcome(console)
        
        # Tenta carregar estado existente
        state = self.state_manager.load()
        
        if state:
            console.print(f"\n[green]✓[/green] Estado carregado: {state.goal}")
            console.print(f"[cyan]Modo:[/cyan] {state.agent_mode}")
            console.print(f"[cyan]Checkpoint:[/cyan] {state.current_checkpoint}")
        else:
            console.print("\n[yellow]Nenhum estado encontrado.[/yellow]")
            goal = Prompt.ask("\nQual é o objetivo desta sessão?")
            state = self.state_manager.create_initial_state(goal)
            console.print(f"\n[green]✓[/green] Estado inicial criado")
        
        self.interactive_loop()
    
    def interactive_loop(self) -> None:
        """Loop principal de interação."""
        while self.running:
            try:
                state = self.state_manager.state
                if not state:
                    break
                
                # Prompt com modo atual
                prompt_text = f"[{state.agent_mode}] > "
                user_input = Prompt.ask(f"\n{prompt_text}").strip()
                
                if not user_input:
                    continue
                
                # Processar comando
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrompido pelo usuário[/yellow]")
                if Prompt.ask("Deseja salvar o estado antes de sair?", choices=["s", "n"]) == "s":
                    console.print("[green]✓[/green] Estado salvo")
                break
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Erro:[/red] {e}")
    
    def process_input(self, user_input: str) -> None:
        """Processa entrada do usuário."""
        # Comandos começam com /
        if user_input.startswith("/"):
            self.handle_command(user_input)
        else:
            # Entrada natural - processar como tarefa
            console.print("[yellow]Processamento de linguagem natural ainda não implementado.[/yellow]")
            console.print("Use comandos / ou aguarde implementação futura.")
    
    def handle_command(self, cmd: str) -> None:
        """Processa comandos /."""
        # Remover / inicial e dividir
        parts = cmd[1:].split(maxsplit=1)
        
        # Validar se há comando (previne erro ao digitar apenas /)
        if not parts or not parts[0]:
            console.print("[yellow]Digite um comando após /[/yellow]")
            console.print("Exemplo: /help, /status, /agent IMPLEMENTER")
            console.print("Digite /help para ver todos os comandos.")
            return
        
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        handlers = {
            "agent": self.command_handler.cmd_agent,
            "workspace": self.command_handler.cmd_workspace,
            "status": self.command_handler.cmd_status,
            "plan": self.command_handler.cmd_plan,
            "resume": self.command_handler.cmd_resume,
            "dry-run": self.command_handler.cmd_dry_run,
            "apply": self.command_handler.cmd_apply,
            "watch": self.command_handler.cmd_watch,
            "undo": self.command_handler.cmd_undo,
            "help": self.command_handler.cmd_help,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
        }
        
        handler = handlers.get(command)
        if handler:
            handler(args)
        else:
            console.print(f"[red]Comando desconhecido:[/red] /{command}")
            console.print("Digite /help para ver comandos disponíveis.")
    
    def cmd_exit(self, args: str = "") -> None:
        """Sai do CLI."""
        console.print("\n[cyan]Até logo![/cyan]")
        self.running = False


@click.command()
@click.option(
    "--workspace",
    "-w",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Diretório de trabalho"
)
@click.option(
    "--goal",
    "-g",
    help="Objetivo da sessão (cria estado inicial)"
)
@click.option(
    "--mode",
    "-m",
    type=click.Choice([m.value for m in AgentMode]),
    default=AgentMode.ARCHITECT.value,
    help="Modo inicial do agente"
)
@click.version_option()
def main(workspace: Optional[str], goal: Optional[str], mode: str) -> None:
    """Perplexity Agent CLI - Sistema de agente com checkpoints."""
    
    cli = PerplexityCLI(workspace)
    
    # Se goal foi fornecido, criar estado inicial
    if goal:
        cli.state_manager.create_initial_state(goal, mode)
    
    cli.start()


if __name__ == "__main__":
    main()
