"""Handlers de comandos do CLI."""

from typing import Optional
from pathlib import Path
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from .state import StateManager
from .models import AgentMode, AGENT_PROFILES
from .utils import print_state, print_plan


class CommandHandler:
    """Handler para comandos do CLI."""
    
    def __init__(self, state_manager: StateManager, console: Console):
        self.state_manager = state_manager
        self.console = console
    
    def cmd_agent(self, args: str) -> None:
        """Troca modo do agente."""
        if not args:
            self.console.print("[red]Uso:[/red] /agent <modo>")
            self.console.print("Modos disponíveis: ARCHITECT, IMPLEMENTER, DEBUGGER, REVIEWER, DOCUMENTER, OPS")
            return
        
        mode_str = args.upper()
        
        try:
            mode = AgentMode(mode_str)
        except ValueError:
            self.console.print(f"[red]Modo inválido:[/red] {mode_str}")
            return
        
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return
        
        old_mode = state.agent_mode
        state.agent_mode = mode.value
        self.state_manager.save(state)
        
        profile = AGENT_PROFILES[mode]
        
        self.console.print(f"\n[green]✓[/green] Modo alterado: {old_mode} → {mode.value}")
        self.console.print(f"\n[cyan]{profile.description}[/cyan]")
        self.console.print(f"\n[bold]Foco:[/bold]")
        for item in profile.focus:
            self.console.print(f"  • {item}")
    
    def cmd_workspace(self, args: str) -> None:
        """Muda workspace."""
        if not args:
            state = self.state_manager.state
            if state:
                self.console.print(f"[cyan]Workspace atual:[/cyan] {state.workspace}")
            return
        
        path = Path(args).resolve()
        
        if not path.exists():
            self.console.print(f"[red]Erro:[/red] Caminho não existe: {path}")
            return
        
        if not path.is_dir():
            self.console.print(f"[red]Erro:[/red] Não é um diretório: {path}")
            return
        
        state = self.state_manager.state
        if state:
            state.workspace = str(path)
            self.state_manager.workspace = str(path)
            self.state_manager.save(state)
            self.console.print(f"[green]✓[/green] Workspace alterado: {path}")
            
            # Listar conteúdo
            try:
                items = list(path.iterdir())
                self.console.print(f"\n[cyan]Conteúdo ({len(items)} itens):[/cyan]")
                for item in items[:10]:
                    icon = "📁" if item.is_dir() else "📄"
                    self.console.print(f"  {icon} {item.name}")
                if len(items) > 10:
                    self.console.print(f"  ... e mais {len(items)-10} itens")
            except Exception as e:
                self.console.print(f"[yellow]Aviso:[/yellow] Não foi possível listar: {e}")
    
    def cmd_status(self, args: str) -> None:
        """Mostra status atual."""
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return
        
        print_state(self.console, state)
    
    def cmd_plan(self, args: str) -> None:
        """Mostra plano atual."""
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return
        
        if not state.plan:
            self.console.print("[yellow]Nenhum plano definido ainda.[/yellow]")
            return
        
        print_plan(self.console, state)
    
    def cmd_resume(self, args: str) -> None:
        """Retoma do último checkpoint."""
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return
        
        self.console.print(f"[cyan]Retomando de:[/cyan] {state.last_successful_checkpoint}")
        self.console.print(f"[cyan]Próxima ação:[/cyan] {state.next_action}")
        
        if state.last_error:
            self.console.print(f"\n[yellow]⚠ Último erro:[/yellow]")
            self.console.print(f"  Local: {state.last_error.get('where', 'N/A')}")
            self.console.print(f"  Mensagem: {state.last_error.get('message', 'N/A')}")
    
    def cmd_dry_run(self, args: str) -> None:
        """Ativa/desativa modo dry-run."""
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return
        
        if args.lower() in ["on", "true", "1"]:
            state.dry_run = True
            self.console.print("[green]✓[/green] Modo dry-run ATIVADO (sem alterações reais)")
        elif args.lower() in ["off", "false", "0"]:
            state.dry_run = False
            self.console.print("[green]✓[/green] Modo dry-run DESATIVADO")
        else:
            status = "ATIVO" if state.dry_run else "INATIVO"
            self.console.print(f"[cyan]Dry-run:[/cyan] {status}")
            return
        
        self.state_manager.save(state)
    
    def cmd_apply(self, args: str) -> None:
        """Aplica patches pendentes."""
        self.console.print("[yellow]Funcionalidade ainda não implementada.[/yellow]")
    
    def cmd_watch(self, args: str) -> None:
        """Liga/desliga watcher."""
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return
        
        if args.lower() in ["on", "true", "1"]:
            state.watch_enabled = True
            self.console.print("[green]✓[/green] Watcher ATIVADO")
            self.console.print("[yellow]Nota:[/yellow] Implementação do watcher pendente")
        elif args.lower() in ["off", "false", "0"]:
            state.watch_enabled = False
            self.console.print("[green]✓[/green] Watcher DESATIVADO")
        else:
            status = "ATIVO" if state.watch_enabled else "INATIVO"
            self.console.print(f"[cyan]Watcher:[/cyan] {status}")
            return
        
        self.state_manager.save(state)
    
    def cmd_undo(self, args: str) -> None:
        """Desfaz últimas alterações."""
        self.console.print("[yellow]Funcionalidade ainda não implementada.[/yellow]")
        self.console.print("Sugestão: use git checkout/restore manualmente")
    
    def cmd_help(self, args: str) -> None:
        """Mostra ajuda."""
        table = Table(title="Comandos Disponíveis")
        table.add_column("Comando", style="cyan")
        table.add_column("Descrição")
        
        commands = [
            ("/agent <modo>", "Troca modo do agente (ARCHITECT, IMPLEMENTER, etc.)"),
            ("/workspace <path>", "Muda workspace ou mostra atual"),
            ("/status", "Mostra estado atual completo"),
            ("/plan", "Mostra plano e checkpoints"),
            ("/resume", "Retoma do último checkpoint"),
            ("/dry-run on|off", "Ativa/desativa modo simulação"),
            ("/apply", "Aplica patches pendentes"),
            ("/watch on|off", "Liga/desliga watcher de arquivos"),
            ("/undo", "Desfaz últimas alterações"),
            ("/help", "Mostra esta ajuda"),
            ("/exit ou /quit", "Sai do CLI"),
        ]
        
        for cmd, desc in commands:
            table.add_row(cmd, desc)
        
        self.console.print(table)
        
        self.console.print("\n[bold]Modos de Agente:[/bold]")
        for mode, profile in AGENT_PROFILES.items():
            self.console.print(f"\n[cyan]{mode.value}[/cyan]: {profile.description}")
