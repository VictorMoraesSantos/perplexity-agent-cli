"""Utilitários e helpers."""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
import json

from .state import RunState


def print_welcome(console: Console) -> None:
    """Imprime mensagem de boas-vindas."""
    welcome_text = """
    [bold cyan]Perplexity Agent CLI[/bold cyan]
    
    Sistema de agente de engenharia com checkpoints e rastreabilidade.
    
    Digite /help para ver comandos disponíveis.
    """
    console.print(Panel(welcome_text, border_style="cyan"))


def print_state(console: Console, state: RunState) -> None:
    """Imprime estado completo."""
    # Painel principal
    console.print("\n[bold]Estado Atual[/bold]\n")
    
    # Tabela de informações básicas
    table = Table(show_header=False, box=None)
    table.add_column("Campo", style="cyan")
    table.add_column("Valor")
    
    table.add_row("Objetivo", state.goal)
    table.add_row("Modo", state.agent_mode)
    table.add_row("Workspace", state.workspace)
    table.add_row("Passo atual", str(state.current_plan_step))
    table.add_row("Checkpoint", state.current_checkpoint)
    table.add_row("Último sucesso", state.last_successful_checkpoint)
    table.add_row("Dry-run", "SIM" if state.dry_run else "NÃO")
    table.add_row("Watch", "ATIVO" if state.watch_enabled else "INATIVO")
    
    console.print(table)
    
    # Próxima ação
    if state.next_action:
        console.print(f"\n[bold]Próxima ação:[/bold] {state.next_action}")
    
    # Arquivos tocados
    if state.files_touched:
        console.print(f"\n[bold]Arquivos modificados ({len(state.files_touched)}):[/bold]")
        for f in state.files_touched[-10:]:
            console.print(f"  • {f}")
        if len(state.files_touched) > 10:
            console.print(f"  ... e mais {len(state.files_touched)-10}")
    
    # Último erro
    if state.last_error:
        console.print(f"\n[yellow]⚠ Último erro:[/yellow]")
        console.print(f"  Quando: {state.last_error.get('when', 'N/A')}")
        console.print(f"  Local: {state.last_error.get('where', 'N/A')}")
        console.print(f"  Mensagem: {state.last_error.get('message', 'N/A')}")
    
    # Questões abertas
    if state.open_questions:
        console.print(f"\n[bold]Questões abertas:[/bold]")
        for q in state.open_questions:
            console.print(f"  ? {q}")
    
    # Comandos executados (últimos 5)
    if state.commands_run:
        console.print(f"\n[bold]Comandos recentes:[/bold]")
        for cmd in state.commands_run[-5:]:
            status_icon = "✓" if cmd.get('result') == 'ok' else "✗"
            status_color = "green" if cmd.get('result') == 'ok' else "red"
            console.print(f"  [{status_color}]{status_icon}[/{status_color}] {cmd.get('cmd', 'N/A')}")


def print_plan(console: Console, state: RunState) -> None:
    """Imprime plano com checkpoints."""
    console.print("\n[bold]Plano de Execução[/bold]\n")
    
    if not state.plan:
        console.print("[yellow]Nenhum plano definido.[/yellow]")
        return
    
    for i, step in enumerate(state.plan, 1):
        # Marcar passo atual
        prefix = "▶" if i == state.current_plan_step else " "
        
        # Verificar se é checkpoint
        if step.startswith("CP"):
            # É um checkpoint
            checkpoint_name = step.split(":")[0] if ":" in step else step
            is_done = state.checkpoints.get(checkpoint_name, False)
            icon = "✓" if is_done else "○"
            color = "green" if is_done else "yellow"
            console.print(f"  {prefix} [{color}]{icon}[/{color}] [bold]{step}[/bold]")
        else:
            # Passo normal
            console.print(f"  {prefix} • {step}")
    
    # Progresso
    completed = sum(1 for v in state.checkpoints.values() if v)
    total_checkpoints = len([s for s in state.plan if s.startswith("CP")])
    
    if total_checkpoints > 0:
        progress = (completed / total_checkpoints) * 100
        console.print(f"\n[cyan]Progresso:[/cyan] {completed}/{total_checkpoints} checkpoints ({progress:.0f}%)")


def format_json(data: dict) -> str:
    """Formata JSON de forma legível."""
    return json.dumps(data, indent=2, ensure_ascii=False)
