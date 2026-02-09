"""Pipeline de execução em etapas com checkpoints."""

from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .state import StateManager, RunState
from .models import AgentMode, AGENT_PROFILES
from .error_protocol import ErrorProtocol


@dataclass
class ExecutionStep:
    """Passo de execução."""
    name: str
    description: str
    action: Callable
    checkpoint: Optional[str] = None


class ExecutionPipeline:
    """Pipeline de execução em etapas (A-E)."""
    
    def __init__(self, state_manager: StateManager, console: Console):
        self.state_manager = state_manager
        self.console = console
        self.error_protocol = ErrorProtocol(state_manager, console)
    
    def execute_task(self, task_description: str) -> bool:
        """Executa tarefa completa seguindo pipeline A-E."""
        state = self.state_manager.state
        if not state:
            self.console.print("[red]Erro:[/red] Nenhum estado carregado")
            return False
        
        self.console.print(f"\n[bold cyan]Iniciando tarefa:[/bold cyan] {task_description}\n")
        
        # Etapa A: Entendimento e critérios
        if not self.step_a_understanding(task_description):
            return False
        
        # Etapa B: Inventário
        if not self.step_b_inventory():
            return False
        
        # Etapa C: Plano
        if not self.step_c_plan():
            return False
        
        # Etapa D: Execução incremental
        if not self.step_d_execution():
            return False
        
        # Etapa E: Fechamento
        self.step_e_closure()
        
        return True
    
    def step_a_understanding(self, task: str) -> bool:
        """Etapa A: Entendimento e critérios de pronto."""
        self.console.print("[bold]Etapa A — Entendimento[/bold]\n")
        
        state = self.state_manager.state
        profile = AGENT_PROFILES[AgentMode(state.agent_mode)]
        
        # Reescrever objetivo baseado no perfil do agente
        self.console.print(f"[cyan]Modo:[/cyan] {state.agent_mode}")
        self.console.print(f"[cyan]Foco:[/cyan] {', '.join(profile.focus[:3])}")
        self.console.print(f"\n[bold]Objetivo reescrito:[/bold]")
        self.console.print(f"  {task}\n")
        
        # Critérios de pronto (exemplo genérico)
        self.console.print("[bold]Critérios de Pronto (DoD):[/bold]")
        criteria = self._generate_dod(state.agent_mode, task)
        for criterion in criteria:
            self.console.print(f"  • {criterion}")
        
        state.next_action = "Executar inventário do workspace"
        self.state_manager.save(state)
        
        return True
    
    def step_b_inventory(self) -> bool:
        """Etapa B: Inventário rápido."""
        self.console.print("\n[bold]Etapa B — Inventário[/bold]\n")
        
        state = self.state_manager.state
        
        # Simulação - em implementação real, faria:
        # - list_dir recursivo
        # - git status
        # - grep por termos relevantes
        
        self.console.print(f"[cyan]Workspace:[/cyan] {state.workspace}")
        self.console.print("[yellow]Nota:[/yellow] Inventário automático será implementado")
        
        state.next_action = "Criar plano com checkpoints"
        self.state_manager.save(state)
        
        return True
    
    def step_c_plan(self) -> bool:
        """Etapa C: Criar plano com checkpoints."""
        self.console.print("\n[bold]Etapa C — Planejamento[/bold]\n")
        
        state = self.state_manager.state
        
        # Gerar plano baseado no agente
        plan = self._generate_plan(state.agent_mode, state.goal)
        state.plan = plan
        state.current_plan_step = 1
        
        self.console.print("[bold]Plano gerado:[/bold]")
        for i, step in enumerate(plan, 1):
            if step.startswith("CP"):
                self.console.print(f"  {i}. [bold yellow]{step}[/bold yellow]")
            else:
                self.console.print(f"  {i}. {step}")
        
        state.next_action = "Executar primeiro passo do plano"
        self.state_manager.save(state)
        
        return True
    
    def step_d_execution(self) -> bool:
        """Etapa D: Execução incremental."""
        self.console.print("\n[bold]Etapa D — Execução Incremental[/bold]\n")
        
        state = self.state_manager.state
        
        self.console.print("[yellow]Execução incremental com validação será implementada[/yellow]")
        self.console.print("Fluxo esperado:")
        self.console.print("  1. Ler arquivos-alvo")
        self.console.print("  2. Aplicar mudanças (patch/write)")
        self.console.print("  3. Validar (git diff, build, test)")
        self.console.print("  4. Atualizar checkpoint")
        self.console.print("  5. Repetir para próximo item")
        
        state.next_action = "Validar resultado e fechar tarefa"
        self.state_manager.save(state)
        
        return True
    
    def step_e_closure(self) -> None:
        """Etapa E: Fechamento."""
        self.console.print("\n[bold]Etapa E — Fechamento[/bold]\n")
        
        state = self.state_manager.state
        
        # Resumo
        self.console.print("[green]✓[/green] Tarefa concluída\n")
        
        if state.files_touched:
            self.console.print(f"[bold]Arquivos alterados ({len(state.files_touched)}):[/bold]")
            for f in state.files_touched:
                self.console.print(f"  • {f}")
        
        self.console.print("\n[bold]Próximos passos:[/bold]")
        self.console.print("  1. Revisar mudanças com /status")
        self.console.print("  2. Testar funcionalidades")
        self.console.print("  3. Fazer commit das alterações")
        
        state.next_action = "Aguardando nova tarefa"
        self.state_manager.save(state)
    
    def _generate_dod(self, agent_mode: str, task: str) -> List[str]:
        """Gera critérios de pronto baseado no agente."""
        # Simplificado - em implementação real seria mais sofisticado
        base_criteria = [
            "Código compila sem erros",
            "Testes passam",
            "Documentação atualizada",
        ]
        
        mode_specific = {
            "ARCHITECT": ["Estrutura de pastas criada", "Interfaces definidas"],
            "IMPLEMENTER": ["Features implementadas", "Código revisado"],
            "DEBUGGER": ["Bug reproduzido", "Correção aplicada", "Regressão testada"],
            "REVIEWER": ["Code review completo", "Sugestões documentadas"],
            "DOCUMENTER": ["README atualizado", "Exemplos adicionados"],
            "OPS": ["CI configurado", "Scripts funcionando"],
        }
        
        return base_criteria + mode_specific.get(agent_mode, [])
    
    def _generate_plan(self, agent_mode: str, goal: str) -> List[str]:
        """Gera plano baseado no agente."""
        # Simplificado - plano genérico
        plan = [
            "Analisar requisitos",
            "Checkpoint: CP1:analysis-complete",
            "Implementar mudanças",
            "Checkpoint: CP2:implementation-done",
            "Validar resultado",
            "Checkpoint: CP3:validated",
        ]
        return plan
