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
from .nlp import IntentDetector


console = Console()


class PerplexityCLI:
    """Classe principal do CLI."""
    
    def __init__(self, workspace: Optional[str] = None, auto_mode: bool = True):
        self.workspace = workspace or os.getcwd()
        self.state_manager = StateManager(self.workspace)
        self.command_handler = CommandHandler(self.state_manager, console)
        self.running = True
        self.auto_mode = auto_mode  # Detecção automática de modo
        
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
            console.print("\n[yellow]✓ Sessão iniciada em modo AUTO[/yellow]")
            console.print("[dim]Digite seu comando em linguagem natural ou use /help[/dim]")
            console.print("[dim]Exemplos: 'criar uma API REST', 'adicionar testes', 'corrigir bug no auth.py'[/dim]")
        
        self.interactive_loop()
    
    def interactive_loop(self) -> None:
        """Loop principal de interação."""
        while self.running:
            try:
                state = self.state_manager.state
                
                # Prompt dinâmico
                if state and not self.auto_mode:
                    prompt_text = f"[{state.agent_mode}] > "
                else:
                    prompt_text = "[AUTO] > "
                
                user_input = Prompt.ask(f"\n{prompt_text}").strip()
                
                if not user_input:
                    continue
                
                # Processar comando
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrompido pelo usuário[/yellow]")
                self.running = False
                break
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Erro:[/red] {e}")
                import traceback
                console.print(f"[dim]{traceback.format_exc()}[/dim]")
    
    def process_input(self, user_input: str) -> None:
        """Processa entrada do usuário."""
        # Comandos começam com /
        if user_input.startswith("/"):
            self.handle_command(user_input)
        else:
            # Entrada natural - processar com NLP
            self.handle_natural_input(user_input)
    
    def handle_natural_input(self, text: str) -> None:
        """Processa entrada em linguagem natural."""
        # Detectar modo apropriado
        detected_mode = IntentDetector.detect_mode(text)
        
        # Extrair objetivo
        goal = IntentDetector.extract_goal(text)
        
        # Mostrar detecção
        console.print(f"\n[cyan]→ Modo detectado:[/cyan] [bold]{detected_mode.value}[/bold]")
        console.print(f"[cyan]→ Objetivo:[/cyan] {goal}")
        
        # Criar ou atualizar estado
        if not self.state_manager.state:
            self.state_manager.create_initial_state(goal, detected_mode.value)
        else:
            # Atualizar goal e modo
            self.state_manager.state.goal = goal
            self.state_manager.state.agent_mode = detected_mode.value
        
        # Salvar estado
        self.state_manager.save()
        
        # Mostrar perfil do agente
        profile = AGENT_PROFILES[detected_mode]
        console.print(f"\n[yellow]Foco:[/yellow] {profile.description}")
        
        console.print("\n[green]✓ Pronto para executar![/green]")
        console.print("[dim]Use /plan para ver o plano, /status para estado atual[/dim]")
        console.print("[dim]Ou continue dando comandos naturais[/dim]")
    
    def handle_command(self, cmd: str) -> None:
        """Processa comandos /."""
        # Remover / inicial e dividir
        parts = cmd[1:].split(maxsplit=1)
        
        # Validar se há comando
        if not parts or not parts[0]:
            console.print("[yellow]Digite um comando após /[/yellow]")
            console.print("Exemplo: /help, /status, /agent IMPLEMENTER")
            console.print("Ou digite em linguagem natural sem /")
            return
        
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Comando especial: modo manual
        if command == "auto":
            if args.lower() == "off":
                self.auto_mode = False
                console.print("[yellow]Modo AUTO desativado. Use /agent para trocar manualmente.[/yellow]")
            else:
                self.auto_mode = True
                console.print("[green]Modo AUTO ativado. Agente será detectado automaticamente.[/green]")
            return
        
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
            # Desativar auto_mode se trocar manualmente
            if command == "agent":
                self.auto_mode = False
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
    help="Objetivo da sessão (modo legado, prefira linguagem natural)"
)
@click.option(
    "--mode",
    "-m",
    type=click.Choice([m.value for m in AgentMode]),
    help="Forçar modo específico (desativa AUTO)"
)
@click.option(
    "--no-auto",
    is_flag=True,
    help="Desativar detecção automática de modo"
)
@click.version_option(version="0.1.0")
def main(workspace: Optional[str], goal: Optional[str], mode: Optional[str], no_auto: bool) -> None:
    """Perplexity Agent CLI - Sistema de agente com checkpoints.
    
    Modo padrão: AUTO - detecta automaticamente o agente baseado no que você digita.
    
    Exemplos:
    
        perplexity-cli
        > criar uma API REST em Python
        
        perplexity-cli
        > adicionar testes unitários
        
        perplexity-cli
        > corrigir bug no arquivo auth.py
    """
    
    auto_mode = not no_auto and mode is None
    cli = PerplexityCLI(workspace, auto_mode=auto_mode)
    
    # Modo legado: goal fornecido
    if goal:
        mode_to_use = mode or AgentMode.ARCHITECT.value
        cli.state_manager.create_initial_state(goal, mode_to_use)
        cli.auto_mode = False
    
    cli.start()


if __name__ == "__main__":
    main()
