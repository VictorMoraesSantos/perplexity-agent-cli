"""Pipeline de execução A-E."""

from typing import List, Dict, Any, Optional
from rich.console import Console

from .state import StateManager, RunState
from .models import AgentMode


class ExecutionPipeline:
    """Pipeline estruturado de execução (Etapas A-E)."""
    
    def __init__(self, state_manager: StateManager, console: Optional[Console] = None):
        self.state_manager = state_manager
        self.state = state_manager.state
        self.console = console or Console()
        self.criteria: List[str] = []
        self.plan: List[Dict[str, Any]] = []
    
    def define_criteria(self, criteria: List[str]) -> None:
        """Etapa A: Define critérios de sucesso.
        
        Args:
            criteria: Lista de critérios de DoD (Definition of Done)
        """
        self.criteria = criteria
        self.console.print("[bold cyan]Etapa A - Critérios Definidos:[/bold cyan]")
        for i, criterion in enumerate(criteria, 1):
            self.console.print(f"  {i}. {criterion}")
    
    def inventory_repo(self) -> Dict[str, Any]:
        """Etapa B: Faz inventário do repositório.
        
        Returns:
            Dicionário com estrutura do repo
        """
        self.console.print("\n[bold cyan]Etapa B - Inventário do Repositório:[/bold cyan]")
        
        import os
        from pathlib import Path
        
        workspace = Path(self.state_manager.workspace)
        
        inventory = {
            'folders': [],
            'files': [],
            'git_status': 'N/A'
        }
        
        # Listar pastas
        for root, dirs, files in os.walk(workspace):
            # Ignorar pastas ocultas e comuns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            rel_root = os.path.relpath(root, workspace)
            if rel_root != '.':
                inventory['folders'].append(rel_root)
            
            for file in files:
                if not file.startswith('.'):
                    rel_path = os.path.join(rel_root, file)
                    inventory['files'].append(rel_path if rel_root != '.' else file)
        
        self.console.print(f"  Pastas: {len(inventory['folders'])}")
        self.console.print(f"  Arquivos: {len(inventory['files'])}")
        
        return inventory
    
    def create_plan(self, plan_items: List[Dict[str, Any]]) -> None:
        """Etapa C: Cria plano com checkpoints.
        
        Args:
            plan_items: Lista de itens do plano, cada um com:
                - step: número da etapa
                - action: ação a executar
                - checkpoint: ID do checkpoint (ex: CP1:init)
        """
        self.plan = plan_items
        
        # Atualizar plano no estado
        if self.state_manager.state:
            self.state_manager.state.plan = [
                f"{item['step']}. {item['action']} [CP: {item['checkpoint']}]"
                for item in plan_items
            ]
            self.state_manager.save()
        
        self.console.print("\n[bold cyan]Etapa C - Plano Criado:[/bold cyan]")
        for item in plan_items:
            self.console.print(
                f"  {item['step']}. {item['action']} "
                f"[dim](Checkpoint: {item['checkpoint']})[/dim]"
            )
    
    def execute_step(self, step: int, action: str, checkpoint: Optional[str] = None) -> bool:
        """Etapa D: Executa uma etapa do plano.
        
        Args:
            step: Número da etapa
            action: Ação a executar
            checkpoint: ID do checkpoint para marcar ao concluir
            
        Returns:
            True se executado com sucesso
        """
        self.console.print(f"\n[bold cyan]Etapa D - Executando Passo {step}:[/bold cyan]")
        self.console.print(f"  Ação: {action}")
        
        # Simulação - em implementação real executaria a ação
        self.console.print("  [yellow]Execução simulada[/yellow]")
        
        # Atualizar checkpoint se fornecido
        if checkpoint and self.state_manager.state:
            self.state_manager.update_checkpoint(checkpoint, success=True)
            self.console.print(f"  [green]✓ Checkpoint salvo: {checkpoint}[/green]")
        
        return True
    
    def close_execution(self, files_modified: List[str], next_steps: List[str]) -> None:
        """Etapa E: Fecha execução e documenta resultados.
        
        Args:
            files_modified: Lista de arquivos modificados
            next_steps: Próximas ações sugeridas
        """
        self.console.print("\n[bold cyan]Etapa E - Fechamento:[/bold cyan]")
        
        # Atualizar estado
        if self.state_manager.state:
            for file in files_modified:
                self.state_manager.add_file_touched(file)
            
            if next_steps:
                self.state_manager.state.next_action = next_steps[0]
                self.state_manager.save()
        
        # Exibir sumário
        self.console.print("\n[green]✓ Execução concluída![/green]\n")
        
        if files_modified:
            self.console.print("[bold]Arquivos modificados:[/bold]")
            for file in files_modified:
                self.console.print(f"  • {file}")
        
        if next_steps:
            self.console.print("\n[bold]Próximos passos:[/bold]")
            for i, step in enumerate(next_steps, 1):
                self.console.print(f"  {i}. {step}")
    
    def run_full_pipeline(
        self,
        criteria: List[str],
        plan_items: List[Dict[str, Any]]
    ) -> bool:
        """Executa pipeline completo A-E.
        
        Args:
            criteria: Critérios de sucesso
            plan_items: Itens do plano
            
        Returns:
            True se pipeline executado com sucesso
        """
        try:
            # Etapa A
            self.define_criteria(criteria)
            
            # Etapa B
            self.inventory_repo()
            
            # Etapa C
            self.create_plan(plan_items)
            
            # Etapa D - executar cada item
            for item in plan_items:
                success = self.execute_step(
                    item['step'],
                    item['action'],
                    item.get('checkpoint')
                )
                if not success:
                    return False
            
            # Etapa E
            modified_files = [item.get('file', 'unknown') for item in plan_items]
            next_steps = ["Validar mudanças", "Executar testes"]
            self.close_execution(modified_files, next_steps)
            
            return True
            
        except Exception as e:
            self.console.print(f"[red]Erro no pipeline:[/red] {e}")
            return False
